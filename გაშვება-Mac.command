#!/bin/bash
# მათბოტის გამშვები — ორჯერ დაწკაპუნებით მუშაობს

cd "$(dirname "$0")"

clear
echo ""
echo "   📐  მათბოტი — მათემატიკა VII"
echo "   ─────────────────────────────"
echo ""

# --- Python-ის შემოწმება
if ! command -v python3 &> /dev/null; then
    echo "   ❌ Python ვერ მოიძებნა."
    echo "   ჩამოტვირთე აქედან: https://www.python.org/downloads/"
    echo ""
    read -p "   დახურვისთვის დააჭირე Enter..."
    exit 1
fi

# --- ბიბლიოთეკები
if ! python3 -c "import streamlit, anthropic, sklearn" &> /dev/null; then
    echo "   ⏳ პირველი გაშვება — ვამზადებ საჭირო პროგრამებს."
    echo "      ეს 1-2 წუთს გასტანს, დაელოდე..."
    echo ""
    python3 -m pip install -q -r requirements.txt 2>/dev/null || \
    python3 -m pip install -q --break-system-packages -r requirements.txt
    echo "   ✅ მზადაა."
    echo ""
fi

# --- API გასაღები
if [ -f ".env" ]; then
    export $(grep -v '^#' .env | xargs)
fi

if [ -z "$ANTHROPIC_API_KEY" ]; then
    echo "   🔑 საჭიროა Anthropic-ის API გასაღები."
    echo "      აიღე აქედან: https://console.anthropic.com  (API keys)"
    echo ""
    read -p "   ჩასვი გასაღები და დააჭირე Enter: " key
    echo "ANTHROPIC_API_KEY=$key" > .env
    export ANTHROPIC_API_KEY="$key"
    echo ""
    echo "   ✅ შენახულია — მეორედ აღარ მოგიწევს."
    echo ""
fi

echo "   🚀 ვუშვებ... ბრაუზერი თავისით გაიხსნება."
echo "   (გასაჩერებლად დააჭირე Ctrl+C)"
echo ""

python3 -m streamlit run app.py
