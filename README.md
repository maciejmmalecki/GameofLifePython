<!-- Kod wygenerowany z pomocą GitHub Copilot (AI) - dokumentacja projektu -->
# GameofLifePython
Podzial zadan:

- Dominika Lankiewicz: 
wczytywanie planszy z pliku tekstowego, zaimplementowanie logiki gry i kodu odpowiedzialnego za wykrywanie zapetlenia

- Maciej Małecki: 
zajecie sie uruchomieniem programu z linii polecen, zaimplementowanie kodu odpowiedzialnego za zapis do video i wizualizacje stanu planszy, stworzenie mechanizmu odpowiedzialnego za zatrzymanie symulacji

Instalacja:
- python co najmniej 3.10 lub nowsza wersja
- pip install
git clone https://github.com/maciejmmalecki/GameofLifePython
cd GameofLifePython
python -m venv venv
venv\Scripts\activate (windows)
Jeżeli nie działa to najpierw wpisać:
Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
pip install -e .
pip install -r requirements.txt

Użycie:
game-of-life config.txt
game-of-life config.txt --fps 15 --max-steps 1000