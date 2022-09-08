from upytl import html as h

# flake8: noqa E226

index = {
    h.Html():{
        h.Head():{
            h.Title():"[[app_get('app_name')]]",
                h.Meta(charset='utf-8'):'',
                h.Link(rel='stylesheet', href='https://cdnjs.cloudflare.com/ajax/libs/bulma/0.9.1/css/bulma.min.css'):None, 
            },
            h.Body():{
                h.Nav(Class='navbar is-light', role='navigation'):{
                    h.A(Class='navbar-item',  href="#"):{
                        h.Div(Class='has-text-primary is-size-5 has-text-weight-semibold'):'Home'
                    },
                },
                h.Div(Class = 'columns'):{
                    h.Div(Class='column has-text-centered'):{
                        h.Div(Class='notification is-primary'):'[[msg]]',
                    },
                },
            },
            h.Footer():{
                h.Div(Class='subtitle has-text-centered'): 'This is the footer generated by UPYTL',
            }
        }
    }
