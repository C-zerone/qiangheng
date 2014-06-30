<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet
    xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0"
    xmlns:exsl="http://exslt.org/common"
    >
  <xsl:output method="text"/>
  <xsl:variable name='intent'><xsl:text>  </xsl:text></xsl:variable>
  <xsl:variable name='itemmark'><xsl:text>- </xsl:text></xsl:variable>
  <xsl:variable name='comment'><xsl:text># </xsl:text></xsl:variable>
  <xsl:variable name='tab'><xsl:text>	</xsl:text></xsl:variable>
  <xsl:variable name='newline'><xsl:text>
</xsl:text></xsl:variable>

  <xsl:template match="/瑲珩">
    <xsl:apply-templates select="範本集"/>
  </xsl:template>

  <xsl:template match="範本集">
    <xsl:text>範本集: </xsl:text>
    <xsl:value-of select="$newline" />
    <xsl:for-each select="範本|comment()">
        <xsl:if test="self::範本">
          <xsl:value-of select="$intent" />
          <xsl:value-of select="$itemmark" />
          <xsl:text>名稱: </xsl:text>
          <xsl:text>"</xsl:text>
          <xsl:value-of select="@名稱" />
          <xsl:text>"</xsl:text>
          <xsl:value-of select="$newline" />

          <xsl:value-of select="$intent" />
          <xsl:value-of select="$intent" />
          <xsl:text>比對: </xsl:text>
          <xsl:call-template name="generate-比對" />

          <xsl:if test="組字結構/組字">
            <xsl:call-template name="generate-模式-top-組字">
            </xsl:call-template>
          </xsl:if>
        </xsl:if>
    </xsl:for-each>
  </xsl:template>

  <xsl:template match="comment()">
    <xsl:text># </xsl:text><xsl:value-of select="." />
    <xsl:value-of select="$newline" />
  </xsl:template>

  <xsl:template name="generate-比對">
    <xsl:text>({運算=</xsl:text>
    <xsl:value-of select="比對/組字/@運算" />
    <xsl:text>}</xsl:text>
    <xsl:text> </xsl:text>

    <xsl:for-each select="比對/組字/字根">
      <xsl:text>.</xsl:text>
      <xsl:if test="position()!=last()">
        <xsl:text> </xsl:text>
      </xsl:if>
    </xsl:for-each>
    <xsl:text>)</xsl:text>
    <xsl:value-of select="$newline" />
  </xsl:template>

  <xsl:template name="generate-模式-top-組字">
    <xsl:for-each select="組字結構/組字">
      <xsl:value-of select="$intent" /> <xsl:value-of select="$intent" />
      <xsl:text>模式: </xsl:text>
      <xsl:call-template name="generate-模式-組字" />
      <xsl:value-of select="$newline" />
    </xsl:for-each>
  </xsl:template>

  <xsl:template name="generate-模式-組字">
      <xsl:if test="@運算">
        <xsl:text>(</xsl:text>
        <xsl:value-of select="@運算" />
        <xsl:text> </xsl:text>
        <xsl:for-each select="字根|組字">
          <xsl:if test="name()='組字'">
            <xsl:call-template name="generate-模式-組字" />
          </xsl:if>
          <xsl:if test="name()='字根'">
            <xsl:call-template name="generate-模式-字根" />
          </xsl:if>

          <xsl:if test="position()!=last()">
            <xsl:text> </xsl:text>
          </xsl:if>
        </xsl:for-each>
        <xsl:text>)</xsl:text>
      </xsl:if>
  </xsl:template>

  <xsl:template name="generate-模式-字根">
        <xsl:value-of select="@置換" />
  </xsl:template>
</xsl:stylesheet>

