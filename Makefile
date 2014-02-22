
VERSION	=	0.20
IMLIST	=	cj ar dy bs zm
IMLIST_ONE	=	cj-one ar-one dy-one bs-one zm-one
IMLIST_MULTIPLE	=	cj-multiple ar-multiple dy-multiple bs-multiple zm-multiple
PLATFORM_LIST	=	puretable scim gcin msim
TABLES_PATH	=	tables
PURETABLE_PATH	=	$(TABLES_PATH)/puretable
XML_PATH	=	$(TABLES_PATH)/xml
SCIM_PATH	=	$(TABLES_PATH)/scim
IBUS_PATH	=	$(TABLES_PATH)/ibus
GCIN_PATH	=	$(TABLES_PATH)/gcin
OVIM_PATH	=	$(TABLES_PATH)/ovim
MSIM_PATH	=	$(TABLES_PATH)/msim
TARBALLS_PATH	=	tarballs
XFORM		=	--xform="s:^:qiangheng/:"
ICON_PATH	=	icons/
ICON_ORIGIN_PATH	=	icons/origin/
ICON_PLATFORM_PATH	=	icons/platform/
SCIM_ICON_PATH	=	icons/platform/scim
IBUS_ICON_PATH	=	icons/platform/ibus
GCIN_ICON_PATH	=	icons/platform/gcin
OVIM_ICON_PATH	=	icons/platform/ovim
MSIM_ICON_PATH	=	icons/platform/msim
RELEASE_TYPE_LIST	=	standard all

.PHONY: xml tarballs all-icons

all: xml

$(XML_PATH):
xml:
	mkdir -p $(XML_PATH)
	for im in $(IMLIST);\
	do\
		echo $$im;\
		time src/qiangheng.py -c qhdata/config/$$im-multiple.xml --xml |\
			xalan -xsl xslt/formatOutput.xslt -out $(XML_PATH)/qh$$im.xml -indent 4;\
	done
	touch $(XML_PATH)

imtables: scim ibus gcin ovim msim puretable

scim: $(SCIM_PATH)
$(SCIM_PATH): $(XML_PATH)
	mkdir -p $(SCIM_PATH)
	for im in $(IMLIST);\
	do\
		xalan -xsl xslt/scim.xslt -in tables/xml/qh$$im.xml -param UUID \"`uuidgen`\" -param SERIAL \"`date +%Y%m%d`\" -param ICON_DIR \"/usr/share/scim/icon/\" -param ICON_FILE \"qh$$im.svg\" -out $(SCIM_PATH)/qh$$im.scim;\
		scim-make-table $(SCIM_PATH)/qh$$im.scim -b -o $(SCIM_PATH)/qh$$im.bin;\
	done
	touch $(SCIM_PATH)

ibus: $(IBUS_PATH)
$(IBUS_PATH): $(XML_PATH)
	mkdir -p $(IBUS_PATH)
	mkdir -p tmp
	for im in $(IMLIST);\
	do\
		xalan -xsl xslt/ibus.xslt -in tables/xml/qh$$im.xml -param UUID \"`uuidgen`\" -param SERIAL \"`date +%Y%m%d`\" -param ICON_FILE \"qh$$im.svg\" -out $(IBUS_PATH)/qh$$im.ibus;\
		bash -c "cd tmp; ibus-table-createdb -s ../$(IBUS_PATH)/qh$$im.ibus";\
	done
	cp tmp/*.db $(IBUS_PATH)
	touch $(IBUS_PATH)

gcin: $(GCIN_PATH)
$(GCIN_PATH): $(XML_PATH)
	mkdir -p $(GCIN_PATH)
	for im in $(IMLIST);\
	do\
		time xalan -xsl xslt/gcin.xslt -in $(XML_PATH)/qh$$im.xml -out $(GCIN_PATH)/qh$$im.cin;\
		gcin2tab $(GCIN_PATH)/qh$$im.cin;\
	done
	touch $(GCIN_PATH)

ovim: $(OVIM_PATH)
$(OVIM_PATH): $(XML_PATH)
	mkdir -p $(OVIM_PATH)
	for im in $(IMLIST);\
	do\
		time xalan -xsl xslt/ovim.xslt -in $(XML_PATH)/qh$$im.xml -out $(OVIM_PATH)/qh$$im.cin;\
	done
	touch $(OVIM_PATH)

msim: $(MSIM_PATH)
$(MSIM_PATH): $(XML_PATH)
	mkdir -p $(MSIM_PATH)
	for im in $(IMLIST);\
	do\
		time xalan -xsl xslt/msim.xslt -in $(XML_PATH)/qh$$im.xml -out $(MSIM_PATH)/qh$$im.msim;\
		sed 's/$$'"/`echo \\\r`/" $(MSIM_PATH)/qh$$im.msim > tmp/qh$$im.msim.dos;\
		iconv -f utf-8 -t utf-16le tmp/qh$$im.msim.dos > $(MSIM_PATH)/qh$$im.msim.txt;\
	done
	touch $(MSIM_PATH)

puretable: $(PURETABLE_PATH)
$(PURETABLE_PATH): $(XML_PATH)
	mkdir -p $(PURETABLE_PATH)
	for type in $(RELEASE_TYPE_LIST);\
	do\
		for im in $(IMLIST);\
		do\
			time xalan -xsl xslt/puretable-$$type.xslt -in $(XML_PATH)/qh$$im.xml -out $(PURETABLE_PATH)/qh$$im-$$type.txt;\
		done;\
	done
	touch $(PURETABLE_PATH)

pdf: tex/qiangheng.pdf

tex/qiangheng.pdf: tex/qiangheng.tex
	cd tex; xelatex qiangheng.tex; rm qiangheng.aux  qiangheng.log

all-icons:
	mkdir -p $(SCIM_ICON_PATH) $(GCIN_ICON_PATH) $(OVIM_ICON_PATH) $(MSIM_ICON_PATH) $(IBUS_ICON_PATH)
	for im in $(IMLIST);\
	do\
		inkscape -D -w 48 -h 48 -e $(SCIM_ICON_PATH)/qh$$im.png $(ICON_ORIGIN_PATH)/qh$$im.svg;\
		inkscape -D -w 30 -h 30 -e $(GCIN_ICON_PATH)/qh$$im.png $(ICON_ORIGIN_PATH)/qh$$im.svg;\
		inkscape -D -w 48 -h 48 -e $(OVIM_ICON_PATH)/qh$$im.png $(ICON_ORIGIN_PATH)/qh$$im.svg;\
		cp $(ICON_ORIGIN_PATH)/qh$$im.svg $(IBUS_ICON_PATH)/qh$$im.png;\
	done
	inkscape -D -w 64 -h 64 -e $(ICON_PLATFORM_PATH)/qiangheng.png $(ICON_ORIGIN_PATH)/qiangheng.svg;

tarballs: pre-tarballs pdf tarball-src tarball-all
	make tarball-src VERSION=$(VERSION)
	make xml puretable
	make imtables
	make tarballs-platform VERSION=$(VERSION)
	make tarball-all VERSION=$(VERSION)

pre-tarballs:
	make clean
	mkdir -p $(TARBALLS_PATH)

tarball-src:
	mkdir -p tmp
	svn ls -R > tmp/files.list
	echo tex/qiangheng.pdf >> tmp/files.list
	tar cjf $(TARBALLS_PATH)/qiangheng-src-$(VERSION).tar.bz2 --exclude-vcs --no-recursion $(XFORM) -T tmp/files.list

tarballs-platform: all-icons
	tar cjf $(TARBALLS_PATH)/qiangheng-scim-$(VERSION).tar.bz2 --exclude-vcs $(XFORM) $(SCIM_PATH)/*.bin $(ICON_PATH) tex/qiangheng.pdf README.txt
	tar cjf $(TARBALLS_PATH)/qiangheng-ibus-$(VERSION).tar.bz2 --exclude-vcs $(XFORM) $(IBUS_PATH)/*.db $(ICON_PATH) tex/qiangheng.pdf README.txt
	tar cjf $(TARBALLS_PATH)/qiangheng-gcin-$(VERSION).tar.bz2 --exclude-vcs $(XFORM) $(GCIN_PATH)/*.gtab $(ICON_PATH) tex/qiangheng.pdf README.txt
	tar cjf $(TARBALLS_PATH)/qiangheng-ovim-$(VERSION).tar.bz2 --exclude-vcs $(XFORM) $(OVIM_PATH)/*.cin $(ICON_PATH) tex/qiangheng.pdf README.txt
	tar cjf $(TARBALLS_PATH)/qiangheng-msim-$(VERSION).tar.bz2 --exclude-vcs $(XFORM) $(MSIM_PATH)/*.txt $(ICON_PATH) tex/qiangheng.pdf README.txt

tarball-all:
	tar cjf $(TARBALLS_PATH)/qiangheng-$(VERSION).tar.bz2 --exclude-vcs --exclude=tarballs -C .. qiangheng

clean:
	rm -rf $(ICON_PLATFORM_PATH)
	rm -rf tables/ tmp/ tarballs/
	rm -f `find src -name "*.pyc"`
	rm -f *~ scim/* gcin/* msim/* puretable/* tex/*.aux tex/*.log tex/*.pdf

