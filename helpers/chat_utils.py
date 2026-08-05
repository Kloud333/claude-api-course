# ЩО ЦЕ: спільні helper-функції, які курс будує поступово, модуль за
# модулем. Пізніші notebooks (RAG, Tool Use, Agents) імпортують звідси
# замість копіювання коду в кожен notebook.
#
# СТАТУС: з модуля "Multi-Turn Conversations" — базові 3 функції.
# Далі буде розширюватись (Tool Use змінить chat(), додасть tool-related
# helpers; RAG додасть retrieval-функції тощо).

from anthropic import Anthropic

# Клієнт і модель — спільні для всіх функцій нижче, тому створюємо один раз
# тут, а не в кожному notebook окремо
client = Anthropic()
model = "claude-sonnet-5"


def add_user_message(messages, text):
    """Додає повідомлення від юзера (людини) в кінець списку messages.

    messages змінюється "на місці" (append) — функція нічого не повертає,
    бо список у Python передається за посиланням.
    """
    user_message = {"role": "user", "content": text}
    messages.append(user_message)


def add_assistant_message(messages, text):
    """Додає повідомлення від Claude (згенерований текст) у кінець messages.

    Викликається ПІСЛЯ отримання відповіді від chat() — щоб Claude в
    наступному запиті "пам'ятав", що сам щойно сказав.
    """
    assistant_message = {"role": "assistant", "content": text}
    messages.append(assistant_message)


def chat(messages):
    """Шле весь список messages до Claude і повертає тільки текст відповіді.

    Приймає ПОВНУ історію розмови (не тільки останнє повідомлення) —
    саме так Claude "бачить" контекст попередніх обмінів.
    """
    message = client.messages.create(
        model=model,
        max_tokens=1000,
        messages=messages,
    )

    # ⚠️ ВАЖЛИВО: Claude Sonnet 5 має adaptive thinking УВІМКНЕНИЙ за
    # замовчуванням — модель сама вирішує, чи "думати" перед відповіддю.
    # Коли думає, message.content МІСТИТЬ ThinkingBlock (без .text!) —
    # часто ПЕРШИМ блоком. Тому content[0] НЕ можна брати наосліп —
    # треба шукати саме текстовий блок за полем type.
    for block in message.content:
        if block.type == "text":
            return block.text

    # Якщо текстового блоку взагалі немає (малоймовірно, але про всяк)
    raise ValueError(f"No text block found in response: {message.content}")
