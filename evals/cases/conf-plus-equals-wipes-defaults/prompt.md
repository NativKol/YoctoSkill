Our CI writes a `conf/auto.conf` before building. Last week someone added these lines to
the CI script, and since then `core-image-base` (poky, scarthgap) no longer boots
properly — it looks like half the base system is missing, and the distro features we get
from poky are gone too:

```bitbake
IMAGE_INSTALL += "htop"
DISTRO_FEATURES += "wifi"
```

On developer machines, where the same lines are not present, everything is fine. Why
would two `+=` lines remove things instead of adding them?
