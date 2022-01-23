Ĉi tio estas programo por krei kartaron por esperanta versio de
[Cross Clues](https://boardgamegeek.com/boardgame/300753/cross-clues).

Se vi volas simple havi la PDF vi povas elŝuti ĝin ĉi tie:

- [Versio](https://esperanto.github.io/krucindiko-duflanke.pdf) por printi ambaŭflanke de la paĝo
- [Versio](https://esperanto.github.io/krucindiko-unuflanke.pdf) por printi unuflanke de la paĝo

La PDFoj enhavas nur la kartojn kun la vortoj. Por ludi oni bezonas ankaŭ la kartojn kun la ciferoj kaj literoj. Ĉe BoardGameGeek estas [prova versio](https://boardgamegeek.com/filepage/204044/print-play) en la franca kaj la angla kiun oni povus kombini kun ĉi tiu esperanta versio por havi plenan printeblan version.

Aliokaze, por ruli la skripton oni unue devas instali la dependajn
pakaĵojn. Ĉe Fedora oni povas ruli la jenan komandon:

    sudo dnf install python3-cairo python3

Poste simple rulu la skripton:

    ./krei-kartojn.py

Tio kreos la PDF-ojn kiu nomiĝas `krucindiko-duflanke.pdf` kaj `krucindiko-unuflanke.pdf`.

Se vi volas aldoni aŭ forigi vortojn vi povas redakti la liston en
`vortoj.csv`. La skripto atentas nur la duan kolumnon.
