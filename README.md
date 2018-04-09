# Git Quotes

Incluye una cita célebre aleatoria en tus commits.

## Instalación

```console
$ git clone https://github.com/pwaqo/commitquotes
$ cd commitquotes
$ bash install.sh
```

## TODO

- Dar soporte para python 2.7 y python3.
Solucionar problema python3.

- Ampliar quotes.json mediante categorías y
autores.

- Archivo de configuración. Elegir categorías de
notas, autores favoritos, etc.

- Ampliar funcionalidad en los casos de ammend, merge, etc.
Que esta funcionalidad sea configurable.

- Solucionar problema de actualización de preparecommit-msg.
Cada vez que se cambia, no se actualizan en los repositorios.

Posibilidades:
    - Instalación de un script `git-quotes`
    - Mediante entry-points python
    - `git-quotes activate`
        - Copia el contenido del script en .git/hooks
    - `git-quotes deactivate`
        - Lo elimina / Lo renombra a un .sample

