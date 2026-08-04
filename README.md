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
```bash
jupyter notebook
```
Відкриється браузер → перейди в `notebooks/` → відкрий потрібний файл.

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
- [ ] `03_system_prompts_and_temperature.ipynb` — наступний модуль
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
