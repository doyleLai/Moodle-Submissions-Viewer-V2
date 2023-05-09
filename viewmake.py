import sys
import json
from os import listdir
from os.path import join, isdir
import re

def natural_sort(l): 
    convert = lambda text: int(text) if text.isdigit() else text.lower()
    alphanum_key = lambda key: [convert(c) for c in re.split('([0-9]+)', key)]
    return sorted(l, key=alphanum_key)

htmltemplate = r"""
<!DOCTYPE html>
<html>
<head>
    <title>Submissions Viewer</title>
    <style>
        * {
            margin: 0px;
            padding: 0px;
            border: none;
            box-sizing: border-box;

        }

        body {
            font-family: Helvetica, sans-serif;
        }
        
        li {
            list-style-type: none;
        }

        iframe {
            border: none;
            width: 100%;
            height: 100%;
            display: block;
        }

        .sidenav {
            height: 100%;
            width: 200px;
            position: fixed;
            z-index: 1;
            top: 0;
            left: 0;
            background-color: rgb(230, 255, 240);
            overflow-y: scroll;
            overflow-x: hidden;
        }

        .sidenav li {
            border-bottom: 1px solid rgb(219, 219, 219);
        }

        .sidenav a {
            color: #000;
            padding: 5px 10px;
            text-decoration: none;
            display: block;
        }

        .sidenav a.selected {
            background-color: rgb(0, 13, 129);
            color: #FFF;
        }

        .sidenav a:hover {
            background-color: rgb(0, 13, 129);
            color: #FFF;
        }

        .status {
            height: 28px;
            width: 100%;
            position: fixed;
            z-index: 1;
            top: 0;
            left: 200px;
            background-color: rgb(0, 13, 129);
            color: #FFF;
            padding: 5px 20px;
            overflow: hidden;
        }

        .filesList {
            height: 28px;
            width: 100%;
            position: fixed;
            z-index: 1;
            top: 28px;
            left: 200px;
            background-color: rgb(255, 255, 255);
            color: #000;
            padding: 5px 20px;
            overflow: hidden;
        }

        .filesList span:not(:last-child):after {
            content: " | ";
        }

        .content {
            top: 56px;
            left: 200px;
            right: 0px;
            bottom: 0px;
            margin: 0px;
            position: absolute;
        }
    </style>
    <script>
        var data = {{json_data_here}};
    </script>
    <script src="https://ajax.googleapis.com/ajax/libs/angularjs/1.6.9/angular.min.js"></script>
    <script>
        var app = angular.module('myApp', []);
        app.controller('myCtrl', function ($scope) {
            window.document.title = data.path + " - Submissions Viewer";
            $scope.path = data.path;
            $scope.submissions = data.submissions;
            $scope.selectedSubmission = -1;
            $scope.currentFile = undefined;
            $scope.currentFolder = undefined;
            $scope.currentFilesList = undefined;

            $scope.setClickedRow = function (index) {
                console.log(index);
                $scope.selectedSubmission = index;
                $scope.currentFolder = $scope.submissions[index].folder;
                $scope.currentFile = $scope.path + "/" + $scope.submissions[index].folder + "/" + $scope.submissions[index].files[0];
                $scope.currentFilesList = $scope.submissions[index].files;
            }
        });
    </script>
</head>
<body ng-app="myApp" ng-controller="myCtrl">
    <div class="sidenav">
        <ul ng-repeat="s in submissions">
            <li><a href="" ng-class="{true:'selected',false:''}[selectedSubmission==$index]"
                    ng-click="setClickedRow($index)">{{s.name}}</a></li>
        </ul>
    </div>
    <div class="status">
        <p>{{currentFolder}}</p>
    </div>
    <div class="filesList">
        <span ng-repeat="f in currentFilesList">{{f}}</span>
    </div>
    <div class="content">
        <iframe src="{{currentFile}}" name="iframe_view" title="submission view"></iframe>
    </div>
</body>
</html>

"""

def main(folder_path:str):
    data = {
        "path": folder_path,
        "submissions": []
    }

    dirs = [f for f in natural_sort(listdir(folder_path)) if isdir(join(folder_path, f))]
    for dir in dirs:
        data["submissions"].append(
            {
                "name": dir.split("_")[0],
                "folder": dir,
                "files": listdir(folder_path + "/" + dir)
            }
        )

    json_str = json.dumps(data, indent = 4).strip()
    
    output_str = htmltemplate.replace(r"{{json_data_here}}", json_str) 

    f = open(folder_path+".html",'w')
    f.write(output_str)
    f.close()


if __name__ == "__main__":
    if len(sys.argv) > 1:
        main(sys.argv[1])
    else:
        print(f'{sys.argv[0]}: Path of the submissions folder should be given.')
