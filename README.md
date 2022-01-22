Ĉi tio estas programo por krei kartaron por esperanta versio de
[Cross Clues](https://boardgamegeek.com/boardgame/300753/cross-clues).

Se vi volas simple havi la PDF vi povas elŝuti ĝin ĉi tie:

- [Versio](https://esperanto.github.io/krucindiko-duflanke.pdf) por printi ambaŭflanke du la paĝo
- [Versio](https://esperanto.github.io/krucindiko-unuflanke.pdf) por printi unuflanke du la paĝo

Aliokaze, por ruli la skripton oni unue devas instali la dependajn
pakaĵojn. Ĉe Fedora oni povas ruli la jenan komandon:

    sudo dnf install python3-cairo python3

Poste simple rulu la skripton:

    ./krei-kartojn.py

Tio kreos la PDF-ojn kiu nomiĝas `krucindiko-duflanke.pdf` kaj `krucindiko-unuflanke.pdf`.

Se vi volas aldoni aŭ forigi vortojn vi povas redakti la liston en
`vortoj.csv`. La skripto atentas nur la duan kolumnon.
