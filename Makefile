all: srpm

srpm:
	./build.sh

clean:
	git clean -ffd

.PHONY: all srpm clean