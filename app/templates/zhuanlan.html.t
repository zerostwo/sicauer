<!DOCTYPE html>
<html>

<head>
<script>
var _hmt = _hmt || [];
(function() {
     var hm = document.createElement("script");
              hm.src = "https://hm.baidu.com/hm.js?7755cea1ce3f2331435d9abccc484b42";
                              var s = document.getElementsByTagName("script")[0];
                                                       s.parentNode.insertBefore(hm, s);
                                                                                         })();
</script>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, shrink-to-fit=no">
    <title>Zzmath</title>
    <link rel="icon" href="{{ url_for('static', filename = 'favicon.ico') }}" type="image/x-icon">
    <link rel="stylesheet" href="{{ url_for('static', filename='assets/bootstrap/css/bootstrap.min.css') }}">
    <link rel="stylesheet" href="https://fonts.googleapis.com/css?family=Nunito:200,200i,300,300i,400,400i,600,600i,700,700i,800,800i,900,900i">
    <link rel="stylesheet" href="{{ url_for('static', filename='assets/fonts/fontawesome-all.min.css') }}">
    <link rel="stylesheet" href="{{ url_for('static', filename='assets/css/Bootstrap-DataTables.css') }}">
    <link rel="stylesheet" href="{{ url_for('static', filename='assets/css/Data-Table-1.css') }}">
    <link rel="stylesheet" href="{{ url_for('static', filename='assets/css/Data-Table.css') }}">
    <link rel="stylesheet" href="https://cdn.datatables.net/1.10.15/css/dataTables.bootstrap.min.css">
    <link rel="stylesheet" href="https://cdn.datatables.net/1.10.20/css/dataTables.bootstrap4.min.css" crossorigin="anonymous">
    <link rel="stylesheet" href="{{ url_for('static', filename='assets/css/Table-With-Search-1.css') }}">
    <link rel="stylesheet" href="{{ url_for('static', filename='assets/css/Table-With-Search.css') }}">
</head>

<body id="page-top">
    <div id="wrapper">
        <div class="d-flex flex-column" id="content-wrapper">
            <footer class="bg-white sticky-footer"><div class="bootstrap_datatables">
<div class="container py-5">
  <header class="text-center text-black">
    <h1 class="display-4">知乎数学相关专栏排名</h1>
  </header>
  <div class="row py-5">
    <div class="col-lg-12 mx-auto">
      <div class="card rounded shadow border-0">
        <div class="card-body p-5 bg-white rounded">
          <div class="table-responsive">
            <table id="example" style="width:100%" class="table table-striped table-bordered">
              <thead>
                <tr>
                     <th class="text-center">排名</th>
                     <th class="text-center">专栏名</th>
                     <th class="text-center">创建者</th>
                     <th class="text-center">关注数</th>
                     <th class="text-center">文章数</th>
                     <th class="text-center">平均赞同数</th>
                     <th class="text-center">平均评论数</th>
                     <th class="text-center">得分</th>
                </tr>
              </thead>
              <tbody>

{% for i in index %}
                                        <tr>
                                            <td class="text-center">{{ i }}</td>
                                            <td class="text-center"><a class="card-link", href="{{ columnUrls[i-1] }}">{{ columnNames[i-1] }}</a></td>
                                            <td class="text-center"><a class="card-link", href="{{ authorUrls[i-1] }}">{{ authorNames[i-1] }}</a></td>
                                            <td class="text-center">{{ followers[i-1] }}</td>
                                            <td class="text-center">{{ articlesCounts[i-1] }}</td>
                                            <td class="text-center">{{ meanVoteupCounts[i-1] }}</td>
                                            <td class="text-center">{{ meanCommentCounts[i-1] }}</td>
                                            <td class="text-center">{{ columnScores[i-1] }}</td>
                                        </tr>
                                          {% endfor %}
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  </div>
</div>
</div>
                <div class="container my-auto">
                    <div class="text-center my-auto copyright"><span>Copyright © Zzmath 2020</span></div>
                </div>
            </footer>
        </div><a class="border rounded d-inline scroll-to-top" href="#page-top"><i class="fas fa-angle-up"></i></a></div>
    <script src="{{ url_for('static', filename='assets/js/jquery.min.js') }}"></script>
    <script src="{{ url_for('static', filename='assets/bootstrap/js/bootstrap.min.js') }}"></script>
    <script src="{{ url_for('static', filename='assets/js/chart.min.js') }}"></script>
    <script src="{{ url_for('static', filename='assets/js/bs-init.js') }}"></script>
    <script src="https://cdn.datatables.net/1.10.15/js/jquery.dataTables.min.js"></script>
    <script src="https://cdn.datatables.net/1.10.20/js/jquery.dataTables.min.js"></script>
    <script src="https://cdn.datatables.net/1.10.15/js/dataTables.bootstrap.min.js"></script>
    <script src="https://cdn.datatables.net/1.10.20/js/dataTables.bootstrap4.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/jquery-easing/1.4.1/jquery.easing.js"></script>
    <script src="{{ url_for('static', filename='assets/js/Bootstrap-DataTables.js') }}"></script>
    <script src="{{ url_for('static', filename='assets/js/Table-With-Search.js') }}"></script>
    <script src="{{ url_for('static', filename='assets/js/theme.js') }}"></script>
</body>

</html>
