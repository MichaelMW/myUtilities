for f in `grep -L '#!' *.py`; do echo '#!/usr/bin/env python'| cat - $f > temp && mv -f temp $f && chmod +x $f; done

