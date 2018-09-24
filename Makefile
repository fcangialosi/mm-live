.PHONY:
all: 
	npm install
	sed "22iSRC=$(shell pwd)" mm-live > mm-live-tmp
	sudo chmod +x mm-live-tmp
	sudo mv mm-live-tmp /usr/local/bin/mm-live
