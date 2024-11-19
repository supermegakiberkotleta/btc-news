let page = 2;

$('#load-more-btn').on('click', function() {
    $.ajax({
        url: loadMoreNewsUrl,  // переменная URL, которую мы определили в шаблоне
        data: {
            'page': page
        },
        success: function(data) {
            if (data.news.length > 0) {
                data.news.forEach(function(news) {
                    let newsItem = `
                      <div class="col-md-4 news-item">
                        <article class="post-item card border-0 shadow-sm p-3">
                          <div class="image-holder zoom-effect">
                            <a href="#">
                              ${news.image_url ? `<img src="${news.image_url}" alt="${news.title}" class="card-img-top">` : ''}
                            </a>
                          </div>
                          <div class="card-body">
                            <div class="post-meta d-flex text-uppercase gap-3 my-2 align-items-center">
                              <div class="meta-categories"><svg width="16" height="16"><use xlink:href="#category"></use></svg>${news.pub_date}</div>
                              <div class="meta-date"><svg width="16" height="16"><use xlink:href="#calendar"></use></svg>${news.pub_date}</div>
                            </div>
                            <div class="post-header">
                              <h3 class="post-title">
                                <a href="/news/${news.slug}/" class="text-decoration-none">${news.title}</a>
                              </h3>
                            </div>
                          </div>
                        </article>
                      </div>
                    `;
                    $('#load-more-btn').before(newsItem);
                });
                page += 1;
            } else {
                $('#load-more-btn').hide();
            }
        }
    });
});
