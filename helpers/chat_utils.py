# ЩО ЦЕ: спільні helper-функції, які курс будує поступово, модуль за
# модулем. Пізніші notebooks (RAG, Tool Use, Agents) імпортують звідси
# замість копіювання коду в кожен notebook.
#
# СТАТУС: з модуля "Temperature" — chat() тепер приймає temperature
# (опціонально!) і дозволяє override моделі для конкретного виклику.

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


def chat(messages, system=None, temperature=None, model_override=None):
    """Шле messages (+ опційно system, temperature) до Claude, повертає текст.

    system=None і temperature=None за замовчуванням — ОБИДВА передаються
    в params, тільки якщо реально задані. Причина для temperature —
    ЖОРСТКІША за system:

    ⚠️ Claude Sonnet 5 (і будь-яка модель новіша за Opus 4.6) ПОВНІСТЮ
    деприкейтила temperature/top_p/top_k — сам факт наявності поля
    "temperature" у запиті (навіть =1.0!) кидає 400 BadRequestError
    "temperature is deprecated for this model". Ці моделі керують
    варіативністю самі, через adaptive thinking, без зовнішньої "крутилки".

    Якщо реально треба продемонструвати ефект temperature — передай
    model_override на модель, що ЩЕ підтримує параметр, напр.
    "claude-sonnet-4-5-20250929".
    """
    params = {
        "model": model_override or model,
        "max_tokens": 1000,
        "messages": messages,
    }
    if system:
        params["system"] = system
    if temperature is not None:
        params["temperature"] = temperature

    message = client.messages.create(**params)

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
