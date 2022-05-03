**Hur använder jag skriptet?**

**Alternativ 1:**
Öppna din command-line interface (CLI) i mappen som skriptet ligger i och kör kommandot `python main.py <filnamn>` (inklusive filändelse `.s` eller `.asm`), t.ex. `python main.py gauss.s`.

**Alternativ 2:**
Öppna din command-line interface (CLI) i mappen som skriptet ligger i och kör kommandot `python main.py`. Du kommer bli uppmanad att skriva in filnamnet (inklusive filändelse `.s` eller `.asm`). Gör det och tryck enter så kommer skriptet köras.

**OBS!!!**

* Filen du försöker testa (filen du skrivit MIPS assembly i) behöver ligga i mappen ett snäpp utanför den här mappen som skriptet ligger i. Så till exempel kan du ha en mapp `.../projektuppgift` där din assemblyfil ligger i `.../projektuppgift/gauss.s`. Skriptet kommer ligga i `.../projektuppgift/datsystek-gauss/main.py`.

* Skriv inte ut resultatet av ditt program! (kommentera bort printMatrix)

* MARS.jar är moddad till att kunna användas genom command line. Försök ej använda GUI, den är troligtvis trasig. Lösningen kommer ändå kontrolleras genom att inspektera ditt programs minne.
