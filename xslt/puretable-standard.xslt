<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0">
  <xsl:output method="text" encoding="UTF-8" indent="yes"/>

  <xsl:variable name='tab'><xsl:text>	</xsl:text></xsl:variable>
  <xsl:variable name='space'><xsl:text> </xsl:text></xsl:variable>
  <xsl:variable name='newline'><xsl:text>
</xsl:text></xsl:variable>

  <xsl:template match="/">
<!--
    <xsl:call-template name="輸出標题"/>
    <xsl:call-template name="輸出設定"/>
    <xsl:value-of select="$newline"/>
-->
    <xsl:call-template name="輸出編碼對應"/>
  </xsl:template>

  <xsl:template name="輸出標题">
  </xsl:template>

  <xsl:template name="輸出設定">
  </xsl:template>

  <xsl:template name="輸出按鍵對應">
  </xsl:template>

  <xsl:template name="輸出編碼對應">
    <xsl:apply-templates select="輸入法/對應集/對應">
      <xsl:sort select="@按鍵序列"/>
    </xsl:apply-templates>
  </xsl:template>

  <xsl:template match="對應">
    <xsl:if test="@類型 = '標準'">
      <xsl:value-of select="@按鍵序列"/>
      <xsl:value-of select="$tab"/>
      <xsl:value-of select="@字符"/>
      <xsl:value-of select="$newline"/>
    </xsl:if>
  </xsl:template>

</xsl:stylesheet>

