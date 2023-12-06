
SRC=src

.PHONY: all clean cleandict exe fabio_src

all:
	$(MAKE) -C $(SRC)
cleandict:
	$(MAKE) -C $(SRC) cleandict
clean:
	$(MAKE) -C $(SRC) clean
exe:
	$(MAKE) -C $(SRC) exe
fabio_src:
	$(MAKE) -C $(SRC) fabio_src
