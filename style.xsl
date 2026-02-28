<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
  <xsl:template match="/">
    <html>
      <head>
        <title><xsl:value-of select="rss/channel/title"/> - プレビュー</title>
        <style>
          body { font-family: sans-serif; max-width: 800px; margin: auto; padding: 20px; background: #f4f4f4; }
          .item { background: white; padding: 15px; margin-bottom: 10px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
          h1 { color: #333; }
          a { color: #007bff; text-decoration: none; font-weight: bold; }
        </style>
      </head>
      <body>
        <h1><xsl:value-of select="rss/channel/title"/></h1>
        <p><xsl:value-of select="rss/channel/description"/></p>
        <hr/>
        <xsl:for-each select="rss/channel/item">
          <div class="item">
            <a href="{link}"><xsl:value-of select="title"/></a>
            <div style="font-size: 0.8em; color: #666;"><xsl:value-of select="pubDate"/></div>
          </div>
        </xsl:for-each>
      </body>
    </html>
  </xsl:template>
</xsl:stylesheet>
