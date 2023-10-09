# Définition d'un point d'arrê
break *0x006a1790
# Execution du programme
run
# Dump de la page contenant la config en clair
dump binary memory dump  0xc000000000 0xc000800000
# Sortie
quit
