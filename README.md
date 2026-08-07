# 🎓 Claude API Course — навчальний проєкт

Робочий простір для практики курсу **"Building with the Claude API"**.
Один notebook на кожен великий блок курсу — код звідти реально запускаєш
і експериментуєш, а не тільки читаєш.

## 🚀 Setup

**Windows (cmd):**
```
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

**macOS / Linux:**
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Скопіюй `.env.example` → `.env`, встав свій `ANTHROPIC_API_KEY`
(див. модуль "Getting an API key" у шпаргалці, якщо забув як отримати).

**Запуск Jupyter:**

**Варіант A — прямо у VSCode (рекомендую, без браузера):**
Просто відкрий будь-який `.ipynb` з `notebooks/` подвійним кліком у Explorer.
VSCode запропонує обрати kernel ("Select Kernel", правий верхній кут) —
обери `.venv` (той, що зі ★). Клітинки виконуються прямо в редакторі.

**Варіант B — класичний Jupyter у браузері:**
```bash
jupyter notebook
```
Відкриє браузер на `localhost:8888`. **Не змішуй з варіантом A** —
якщо вже відкрив notebook у VSCode, не запускай цю команду одночасно.

## 📁 Структура

```
claude-api-course/
├── .env                              # твій API-ключ (НЕ комітиться)
├── .env.example                      # шаблон
├── requirements.txt                  # залежності (ростуть разом із курсом)
├── notebooks/
│   └── 01_accessing_the_api.ipynb    # Making a Request — перший робочий запит
└── helpers/
    └── chat_utils.py                 # спільні функції (add_user_message, chat()...)
                                       # наповнюється з модуля "Multi-Turn Conversations"
```

## 📌 Статус

- [x] `01_accessing_the_api.ipynb` — setup + перший запит + розбір відповіді
- [x] `02_multi_turn_conversations.ipynb` — helper-функції (`add_user_message`, `add_assistant_message`, `chat`) + приклад "зламаної" розмови без history vs правильної
- [x] `03_chat_exercise.ipynb` — вправа: чат-бот на `while True` + `input()`, + бонусна версія з командою виходу
- [x] `04_system_prompts.ipynb` — math tutor приклад (з/без system prompt), `chat()` тепер приймає `system=None` + System Prompts Exercise (concise code style)
- [x] `05_temperature.ipynb` — low vs high temperature на генерації сюжетів фільму, `chat()` тепер приймає `temperature=1.0`
- [x] `06_response_streaming.ipynb` — сирі events, спрощений text_stream, get_final_message() (напряму через client/model — стрімінг має власну структуру виклику, не через chat())
- [x] `07_structured_data.ipynb` — pre-fill + stop_sequences на EventBridge JSON-прикладі (⚠️ виправлено: Sonnet 5 не підтримує prefill, обхід через `model_override` + бонусний сучасний `output_config`), `chat()` тепер приймає `stop_sequences` і `output_config` + Structured Data Exercise (3 AWS CLI команди в одній відповіді — пастка з одним code block на команду vs детальний prefill-інсайт)
- [ ] `08_prompt_evaluation.ipynb` — наступний модуль
- [ ] ...решта notebooks додаватимуться по одному, синхронно з проходженням курсу

`helpers/chat_utils.py` тепер містить 3 базові функції (client, model,
`add_user_message`, `add_assistant_message`, `chat`) — наступні notebooks
імпортують їх звідси.

> 💡 **Принцип той самий, що й у `cli_project`/`mcp-server-demo`**: структура росте
> поступово, модуль за модулем, а не вся одразу. `helpers/chat_utils.py` буде
> накопичувати функції так само, як курс сам будує їх крок за кроком
> (спочатku `add_user_message`/`add_assistant_message`/`chat()`, потім
> tool-related helpers, потім RAG-функції тощо) — пізніші notebooks
> імпортуватимуть звідти, а не дублюватимуть код.
