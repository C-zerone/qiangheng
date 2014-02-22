
VERSION	=	0.04
IMLIST	=	cj ar dy bs zm
TEST_IMLIST	=	cj ar dy bs zm
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
ICON_PATH	=	icons/ pixmaps/

.PHONY: xml tarballs pixmaps

all: xml

$(XML_PATH):
xml:
	mkdir -p $(XML_PATH)
	for im in $(IMLIST);\
	do\
		echo $$im;\
#		time ./qiangheng.py -i $$im --xml > _$$im.xml;\
		time ./qiangheng.py -i $$im --xml |\
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
	for im in $(IMLIST);\
	do\
		time xalan -xsl xslt/puretable.xslt -in $(XML_PATH)/qh$$im.xml -out $(PURETABLE_PATH)/qh$$im.txt;\
	done
	touch $(PURETABLE_PATH)

testing:
	for im in $(TEST_IMLIST);\
	do ./qiangheng.py --dir-charinfo test/charinfo -i $$im > test/puretable/$$im.puretable.txt;\
	done

compare: testing
	diff -rN test/puretable_ans test/puretable

tex/principle.pdf: tex/principle.tex
	cd tex; xelatex principle.tex; rm principle.aux  principle.log

old-format:
	for i in ar bs cj dy zm main;\
	do\
		xalan -xsl xslt/xml2txt.xslt -in charinfo/$$i/CJK.xml -out charinfo/$$i/CJK.old.txt;\
	done

pixmaps:
	mkdir -p pixmaps
	for im in $(IMLIST);\
	do inkscape -D --export-png\=pixmaps/qh$$im.png icons/qh$$im.svg;\
	done

tarballs: pre-tarballs tarball-src tarball-all
	make tarball-src VERSION=$(VERSION)
	make xml
	make imtables
	make tarballs-platform VERSION=$(VERSION)
	make tarball-all VERSION=$(VERSION)

pre-tarballs:
	make clean
	mkdir -p $(TARBALLS_PATH)

tarball-src:
	mkdir -p tmp
	svn ls -R > tmp/files.list
	echo tex/principle.pdf >> tmp/files.list
	tar cjf $(TARBALLS_PATH)/qiangheng-src-$(VERSION).tar.bz2 --exclude-vcs --no-recursion $(XFORM) -T tmp/files.list

tarballs-platform: pixmaps
	tar cjf $(TARBALLS_PATH)/qiangheng-scim-$(VERSION).tar.bz2 --exclude-vcs $(XFORM) $(SCIM_PATH)/*.bin $(ICON_PATH) README.txt
	tar cjf $(TARBALLS_PATH)/qiangheng-ibus-$(VERSION).tar.bz2 --exclude-vcs $(XFORM) $(IBUS_PATH)/*.db $(ICON_PATH) README.txt
	tar cjf $(TARBALLS_PATH)/qiangheng-gcin-$(VERSION).tar.bz2 --exclude-vcs $(XFORM) $(GCIN_PATH)/*.gtab $(ICON_PATH) README.txt
	tar cjf $(TARBALLS_PATH)/qiangheng-ovim-$(VERSION).tar.bz2 --exclude-vcs $(XFORM) $(OVIM_PATH)/*.cin $(ICON_PATH) README.txt
	tar cjf $(TARBALLS_PATH)/qiangheng-msim-$(VERSION).tar.bz2 --exclude-vcs $(XFORM) $(MSIM_PATH)/*.txt $(ICON_PATH) README.txt

tarball-all:
	tar cjf $(TARBALLS_PATH)/qiangheng-$(VERSION).tar.bz2 --exclude-vcs --exclude=tarballs -C .. qiangheng

clean:
	rm -rf tables/ tmp/ tarballs/ pixmaps
	rm -f charinfo/*/CJK.old.txt
	rm -f *.pyc im/*.pyc character/*.pyc operatorinfo/*.pyc
	rm -f *~ scim/* gcin/* msim/* puretable/* tex/*.aux tex/*.log
	rm -f charinfo/*/*.bak.txt charinfo/*/*.rst.txt
	rm -f test/puretable/*

