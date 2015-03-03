%#template for the form for a new crawl task
<p>Add a new crawl task:</p>
<form action="/controller" method="GET">
<input type="text" size="150" maxlength="250" name="crawl_url">
<input type="submit" name="start_crawl" value="start_crawl">
<p>Start disambiguation:</p>
<input type="submit" name="start_disambiguation" value="start_disambiguation">
</form>
<p> <a href=/pages>Crawled pages</a> </p>
<p> <a href=/nevek>All names</a> </p>
<p> <a href=/alias>Aliases</a> </p>

%rebase layout