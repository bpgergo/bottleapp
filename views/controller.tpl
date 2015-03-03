%#template for the form for a new crawl task
<p>Crawl urls like <a href="http://palatinusbridge.hu/mezhon/eredmenyek/">http://palatinusbridge.hu/mezhon/eredmenyek/</a>
or <a href="http://palatinusbridge.hu/mezhon/eredmenyek/2015palaered/">http://palatinusbridge.hu/mezhon/eredmenyek/2015palaered/</a> </p>
<p>Add a new crawl task:</p>
<form action="/controller" method="GET">

<input type="text" size="150" maxlength="250" name="crawl_url">
<input type="submit" name="start_crawl" value="start_crawl">


<p>Name disambiguation for urls already crawled, like <a href="http://palatinusbridge.hu/mezhon/eredmenyek/2015palaered/">http://palatinusbridge.hu/mezhon/eredmenyek/2015palaered/</a> </p>
<p>Start disambiguation:</p>
<input type="text" size="150" maxlength="250" name="disambiguation_url">
<input type="submit" name="start_disambiguation" value="start_disambiguation">

</form>
<p> <a href=/crawls>Crawles</a> </p>
<p> <a href=/nevek>All names</a> </p>
<p> <a href=/alias>Aliases</a> </p>

%rebase layout