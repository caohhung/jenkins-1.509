all: srpm

srpm:

clean:
	git clean -ffd

.PHONY: all srpm clean