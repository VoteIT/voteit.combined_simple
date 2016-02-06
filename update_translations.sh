 #!/bin/bash
 #You need lingua and gettext installed and in your path to run this
 
 echo "Updating voteit.combined_simple.pot"
 pot-create -d voteit.combined_simple -o voteit/combined_simple/locale/voteit.combined_simple.pot .
 echo "Merging Swedish localisation"
 msgmerge --update voteit/combined_simple/locale/sv/LC_MESSAGES/voteit.combined_simple.po voteit/combined_simple/locale/voteit.combined_simple.pot
 echo "Updated locale files"
 