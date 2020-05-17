#!/usr/bin/env python3

template = \
'''
<!DOCTYPE html>
<html>

<head>
    <title>Hydra Recon Report</title>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.4.1/css/bootstrap.min.css">
</head>

<body>
    {% for host in hosts%}
    <div class="container my-3">
        <div class="row">
            <div class="container col-sm-3 border rounded shadow h-50 p-3 zoom">
                <img src="{{home_path}}/hydra_report/screenshots/{{ host["file_name"]}}.png" class="img-fluid float-left" width="300" height="280">
                <div class="container row">
                    <a>{{host["url"]}}</a>
                </div>
                <div class="container row pl-0 pt-2">
                    <div class="col container-fluid">
                        <a href="{{host['url']}}" class="btn btn-primary btn-sm rounded" target="_blank">Visit Site</a>
                    </div>
                    <div class="col">
                        <button class="btn-sm rounded btn-dark p-1">{{host["status_code"]}}</button>
                    </div>
                </div>
            </div>

            <div class="container-fluid col-md-8">
                <table class="table table-striped table-hover table-responsive">
                    <thead class="thead-dark">
                        <tr>
                            <th>Header</th>
                            <th>Value</th>
                        </tr>
                    </thead>
                    <tbody>
                        {% for key in host["headers"].keys() %}
                        <tr>
                            <td>{{ key }}</td>
                            <td>{{host["headers"][key]}}</td>
                        </tr>
                        {% endfor %}
                    </tbody>
                </table>
            </div>
        </div>
    </div>
    {% endfor %}
</body>

</html>
'''
