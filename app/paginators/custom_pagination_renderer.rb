class CustomPaginationRenderer < WillPaginate::ActionView::LinkRenderer
    protected
  
    def page_number(page)
        if page == current_page
            link(page, '#', class: 'page-link active', 'aria-current': 'page')
          else
            link(page, url(page), class: 'page-link')
          end
          
      end
      
  
    def gap
      text = @template.will_paginate_translate(:page_gap) { '&hellip;' }
      %(<li class="page-item disabled"><a class="page-link" href="#">#{text}</a></li>)
    end
  
    def previous_or_next_page(page, text, classname)
        if page
          link('<span class="ion-ios-arrow-' + (classname == 'previous' ? 'back' : 'forward') + '"></span>', url(page), class: "page-link", aria_label: text, rel: classname)
        else
          tag('li', tag('a', '<span class="ion-ios-arrow-' + (classname == 'previous' ? 'back' : 'forward') + '"></span>', class: "page-link disabled"), class: "page-item #{classname}")
        end
      end
      
      
  
    def html_container(html)
        tag('nav', tag('ul', html, class: 'd-flex justify-content-end'), class: 'pagination')
      end

    def previous_or_next_page(page, text, classname)
  if page
    link(text, url(page), class: "page-link #{classname}")
  else
    tag('li', tag('a', text, class: "page-link #{classname} disabled"), class: 'page-item')
  end
end

  end
  