from deep_translator import GoogleTranslator

kannada_text = "ನಾನು ಕನ್ನಡದಿಂದ ಇಂಗ್ಲಿಷ್‌ಗೆ ಅನುವಾದ ಮಾಡುತ್ತಿದ್ದೇನೆ"
translated_text = GoogleTranslator(source='kn', target='en').translate(kannada_text)
print(translated_text) 