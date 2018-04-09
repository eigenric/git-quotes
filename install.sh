# Script de instalación


confirm() {
    read -p "$1" response
    case "$response" in
        [sS]* ) true;;
        *) false;;
    esac
}

hook_folder="$HOME/.git-templates/hooks"
hook_file="$hook_folder/prepare-commit-msg"


install() {
    if [ ! -e $hook_folder ]; then
        echo "Creando directorio $hook_folder"
        mkdir -p $hook_folder
    else 
        echo "Directorio de hooks existente"
        if [ -e $hook_file ]; then
            echo "Ya tienes un hook de preparación de commit"
            echo "Sólo podrás utilizar este programa si lo sobrescribes"
            confirm "¿Desea sobrescibirlo? (s/N): " || { echo "De acuerdo" && exit; }
        fi
    fi

    echo "Activando directorio de plantillas de git"
    git config --global init.templates '$HOME/.git-templates'
    echo "Moviendo hook y archivo de citas"
    cp prepare-commit-msg $hook_folder
    cp quotes.json $hook_folder
    echo "Otorgando permisos de ejecución"
    chmod +x $hook_file

    echo "Listo!"
    echo "Ahora cada vez que realices git commit (sin la opción -m), se incluirá una 
        frase célebre el mensaje. Estará precedida por una almohadilla luego tendrás
        que descomentar la línea".
}


confirm "Desea instalar commitquotes? (s/N): " && install || exit
