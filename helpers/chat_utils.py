# ЩО ЦЕ: спільні helper-функції, які курс будує поступово, модуль за
# модулем. Пізніші notebooks (RAG, Tool Use, Agents) імпортують звідси
# замість копіювання коду в кожен notebook.
#
# СТАТУС: з модуля "Structured Data" — chat() приймає stop_sequences
# І output_config (сучасна заміна prefill для Sonnet 5+).

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

    ⚠️ Також використовувалась для pre-filling (вручну підставити "початок"
    відповіді асистента). З Claude Sonnet 5 (і будь-якою моделлю новішою
    за 4.5) prefill БІЛЬШЕ НЕ ПІДТРИМУЄТЬСЯ — API вимагає, щоб розмова
    завжди закінчувалась user message. Для prefill-техніки потрібен
    model_override на старшу модель (див. chat()) або сучасна заміна —
    output_config (теж нижче).
    """
    assistant_message = {"role": "assistant", "content": text}
    messages.append(assistant_message)


def chat(
    messages,
    system=None,
    temperature=None,
    stop_sequences=None,
    output_config=None,
    model_override=None,
):
    """Шле messages до Claude, повертає текст. Усі опції — опціональні.

    ⚠️ ДВІ РЕЧІ, ЯКІ НЕ ПРАЦЮЮТЬ З CLAUDE SONNET 5 (модель новіша за 4.6):
    1. temperature — параметр повністю деприкейтений, кидає 400 з будь-яким
       значенням. Обхід: model_override="claude-sonnet-4-5-20250929".
    2. Assistant message prefill (messages, що закінчуються role="assistant")
       — теж кидає 400: "This model does not support assistant message
       prefill. The conversation must end with a user message."
       Обхід А (як у курсі): той самий model_override на старшу модель.
       Обхід Б (сучасний, рекомендований Anthropic): output_config замість
       prefill+stop_sequences — див. приклад нижче.

    output_config: dict формату
        {"format": {"type": "json_schema", "schema": {...звичайна JSON schema...}}}
    — гарантує (schema-validated), що відповідь буде валідним JSON за
    заданою схемою. Це офіційна заміна prefill-техніки для Claude 4.6+.
    ⚠️ schema вимагає "additionalProperties": False на КОЖНОМУ object-рівні
    (і верхньому, і вкладених) + усі properties в "required" — інакше 400.
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
    if stop_sequences:
        params["stop_sequences"] = stop_sequences
    if output_config:
        params["output_config"] = output_config

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
