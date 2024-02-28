from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for,
    current_app
)

from semantic_search_app.lib import get_search_results

bp = Blueprint('search', __name__, url_prefix='/search')

@bp.route('/search', methods=(['GET', 'POST']))
def search():
    query = request.args.get('query', '')

    # Get all titles from the BibTeX file
    # all_titles = parse_bibtex(BIBTEX_FILE)

    # Filter titles based on the query
    # results = [title for title in all_titles if query.lower() in title.lower()]
    data = current_app.config["data"]
    model = current_app.config["model"]
    corpus = current_app.config["corpus"]
    result = get_search_results(model, data, corpus, query, current_app.logger)
    records = []
    for title, url, abstract in result:
        records.append({"title": title, "url": url, "abstract": abstract})
    return {"entries": records}
    # return render_template('index.html', results=results, query=query)

@bp.route('/find', methods=(['GET']))
def find():
    return render_template('index.html')