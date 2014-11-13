
$(function() {

    // A Dataset Model contains the csv string of the dataset
    var DatasetModel = Backbone.Model.extend({ 
        defaults: {
            title: '',
            name: '',  //name of the dataset
            rows: [], //data rows of the dataset
            type: 'csv',
            completed: false 
        },
        getHeader: function() {
            var rows = this.get("rows");
            if ( rows.length > 0 ) {
                if ( this.get('type') === 'csv') {
                    //Add empty header as the first parameter
                    var cp = rows[0].slice(0);
                    cp.unshift('');
                    return cp;

                }
                return rows[0];
            }
            return undefined;
        }
    });

    var DatasetView = Backbone.View.extend({ 
        tagName: 'table',
        className: 'table table-hover',
        id: 'data-table',
        events: {
        },
        // Rerender the titles of the todo item.
        render: function() {
            //TODO : D3 data based updade should be considerred later
            this.$el.empty(); //clean on each render
            var header = d3.select(this.el).append("thead").append("tr").attr("id","data-table-header");
            var body = d3.select(this.el).append("tbody").attr("id","data-table-body");
            var rows = this.model.get("rows");

            header.selectAll("th").data(rows[0]).enter().append("th").text(function(d){
                return d;
            });

            var i = 1, length = rows.length;
            for ( ; i < length; i++) {
                body.append("tr").selectAll("td").data(rows[i])
                    .enter().append("td").text(function(d){
                        return d;
                    });
            }

            return this;
        },
    });

    var RowCSVModel = Backbone.Model.extend({ 
        urlRoot : '/data/',
        url : function(){
            var url = this.urlRoot + this.get("name");
            return url;
        }
    });

    var VizModel = Backbone.Model.extend({
        urlRoot : '/viz',
        defaults: {
            src: '/viz/file.png',
            width: '100%',
            height: '420px'
        }
    });

    var VizView = Backbone.View.extend({ 
        tagName: 'img',
        id: 'viz-img',
        events: {
        },
        // Rerender the titles of the todo item.
        render: function() {
            //this.$el.empty(); //clean on each render
            d3.select(this.el).attr("src",this.model.get("src"));
            d3.select(this.el).attr("height",this.model.get("height"));
            d3.select(this.el).attr("width",this.model.get("width"));

            return this;
        },
    });

    var ControlModel = Backbone.Model.extend({
        defaults: {
            xaxis : [],
            yaxis : [],
            color : [],
            shape : [],
            layer1 : ['','point','bar','line'],
            layer2 : ['','point','bar','line']
        }
    });

    var ControlView = Backbone.View.extend({ 
        tagName: 'div',
        id: 'viz-control',
        events: {
        },
        // Rerender the titles of the todo item.
        render: function() {
            this.$el.empty();

            function renderRow(root,name,label,data) {
                var row = d3.select(root).append('div').classed('row-fluid',true);
                row.append('h4').append('span').classed('label label-info col-md-2',true)
                    .text(label);
                row.append('select').classed('selectpicker col-md-8',true).attr("name",name)
                    .selectAll('option').data(data)
                    .enter().append('option').text(function(d){
                        return d;
                    });
                row.append('span').classed('glyphicon glyphicon-wrench',true); 
            }
            
            renderRow(this.el,"xaxis","X Axis",this.model.get("xaxis"));
            renderRow(this.el,"yaxis","Y Axis",this.model.get("yaxis"));
            renderRow(this.el,"color","Color",this.model.get("color"));
            renderRow(this.el,"shape","Shape",this.model.get("shape"));
            renderRow(this.el,"layer1","Layer1",this.model.get("layer1"));
            renderRow(this.el,"layer2","Layer2",this.model.get("layer2"));

            d3.select(this.el).append('hr');
            var currentEl = this.el;

            var row = d3.select(this.el).append('div').classed('row-fluid',true);
            row.append('h4').append('button').classed('btn btn-default btn-xs col-md-2 col-md-offset-4',true)
                .text('Plot').on('click',function() {
                    console.log("plotting");

                    dataspec = {};
                    dataspec.name = myData.get('name');
                    dataspec.type = myData.get('type');
                    dataspec.viz = {};
                    dataspec.viz.xaxis = $(currentEl).find("[name='xaxis']").find(':selected').text();
                    dataspec.viz.yaxis = $(currentEl).find("[name='yaxis']").find(':selected').text();
                    dataspec.viz.color = $(currentEl).find("[name='color']").find(':selected').text();
                    dataspec.viz.shape = $(currentEl).find("[name='shape']").find(':selected').text();
                    dataspec.viz.layer1 = $(currentEl).find("[name='layer1']").find(':selected').text();
                    dataspec.viz.layer2 = $(currentEl).find("[name='layer2']").find(':selected').text();

                    var aViz = new VizModel();
                    var aVizView = new VizView({model:aViz});
                    aViz.fetch({
                        data: dataspec, 
                        type: 'POST', 
                        success: function(d){
                            $("#viz-panel").empty();
                            $("#viz-panel").append(aVizView.render().el);
                        }
                    });
                });
            return this;
        },
    });


    //Gloable Object Definition
    var myData = new DatasetModel();
    var myDataView = new DatasetView({model:myData});

    //Interaction Logic

    //Data selection
    $(".data_select_menu").click(function(){
        var oneCSV = new RowCSVModel();
        var id = $(this).attr("id");
        var url = "/csvdata";

        if (id === "menu_select_r_data") {
            url = "/rdata";
            oneCSV.urlRoot = "/rdata/";
        }

        //Query Data 
        $.get(url,function(data){
            var dataset_list = JSON.parse(data);
            $("#data_select_panel").empty();
            d3.select("#data_select_panel").selectAll("span").data(dataset_list)
                .enter().append("button").classed("btn btn-primary btn-xs data-select-btn",true).style({"margin":"2px","float":"left"}).text(function(d){
                return d;
            }).on("click",function(d){
                $("#data_select_modal").modal("hide");
                oneCSV.set("name",d);
                oneCSV.fetch({
                    success: (function () {
                        //Clear the current table
                        $("#table-panel").empty();
                        var csvarray = Baby.parse(oneCSV.get("csv"));
                        myData.set("name",d);
                        if (id === "menu_select_r_data") {
                            myData.set('type','R')
                        }
                        //TODO : error handling of parse result
                        // slice the dataset, only show the first 100 rows
                        myData.set("rows",csvarray.data.slice(0, 100));
                        console.log(myData.getHeader())
                        $("#table-panel").append(myDataView.render().el);
                    }),
                    error: (function (e) {
                        console.log("Failed to request data name : " + d);
                    })
                });
            });
            $("#data_select_modal").modal("show");
        })
    });


    //CSV Data Upload
    $("#menu_add_data").click(function(){
        $("#data_upload_modal").modal("show");
        // Refer to http://abandon.ie/notebook/simple-file-uploads-using-jquery-ajax
    });


    //Visualization
    $("#menu_visualization").click(function(){
        var myCtlModel = new ControlModel();
        var myCtlView = new ControlView({model:myCtlModel});

        myCtlModel.set("xaxis",myData.getHeader());
        myCtlModel.set("yaxis",myData.getHeader());
        myCtlModel.set("color",myData.getHeader());
        myCtlModel.set("shape",myData.getHeader());

        $("#control-body").empty();
        $("#control-body").append(myCtlView.render().el);

        //Apply the style after adding to DOM
        $('.selectpicker').selectpicker({
            style: 'btn btn-default btn-xs',
            size: 4
        });
    });
})