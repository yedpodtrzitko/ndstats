var NDProgress = React.createClass({displayName: "NDProgress",
    oldest: React.PropTypes.object,
    newest: React.PropTypes.object,
    current: React.PropTypes.object,
    diff: React.PropTypes.number,
    structures: React.PropTypes.array,
    kills: React.PropTypes.array,
    ctx: React.PropTypes.object,
    value: React.PropTypes.number,
    maxvalue: React.PropTypes.number,

    getInitialState: function () {
        return {
            structures: [],
            kills: [],
            diff: 6,
            oldest: null,
            newest: null,
            ctx: null,
            value: 550,
            timetable: 0,
            maxvalue: 550,
        };
    },

    timeTable: function (value) {
        var timetable = (value * this.state.diff);
        var seconds = Math.round(timetable % 60).toString();
        if (seconds.length < 2) {
            seconds = "0" + seconds;
        }
        var minutes = Math.round(timetable / 60).toString();
        if (minutes.length < 2) {
            minutes = "0" + minutes;
        }
        return minutes + ":" + seconds;
    },

    onChange: function (e) {
        var current = this.state.oldest + (e.target.value * this.state.diff);
        this.setState({
            'current': current,
            'value': e.target.value,
            'timetable': this.timeTable(e.target.value),
        });

        this.renderProgress();
        return true;
    },

    renderProgress: function () {
        var until = this.state.current;
        var structs = this.state.structures;
        var ctx = this.state.ctx;
        for (var i in structs) {
            if (structs[i].item.when > until) {
                if (structs[i].visible) {
                    ctx.removeChild(structs[i]);
                    structs[i].visible = false;
                }
            } else {
                if (!structs[i].visible) {
                    ctx.addChild(structs[i]);
                    structs[i].visible = true;
                }
            }
        }
    },

    render: function () {
        var slider = React.DOM.input({
            type: "range",
            id: "slider",
            min: 0,
            max: this.state.maxvalue,
            value: this.state.value,
            step: 1,
            onChange: this.onChange
        });

        var canvas = React.createElement('canvas', {
            'id': 'map',
            'width': 1000,
            'height': 1000,
        });

        return (
            React.createElement("div", null, 
                canvas, 
                React.createElement("div", {id: "timetable"}, this.state.timetable, " "), 
                slider
            )
        )
    },

    mapResize: function (item) {
        var self = this;
        var fixer = mapData[this.props.map] || function (info) {
                console.log('missing fix for ' + self.props.map);
            };
        fixer(item);
    },

    componentWillMount: function () {
        $.get(this.props.urldata, function (result) {
            if (this.isMounted()) {
                var ctx = new oCanvas.core({
                    canvas: '#map'
                });

                var state = {
                    structures: [],
                    kills: [],
                    oldest: null,
                    newest: null,
                    current: null,
                    ctx: ctx,
                };


                for (var i in result) {
                    var item = result[i];
                    item.when = Date.parse(item.when) / 1000.0;

                    this.mapResize(item);

                    if (!state.oldest || (item.when < state.oldest)) {
                        state.oldest = item.when;
                    }

                    if (!state.newest || (item.when > state.newest)) {
                        state.newest = item.when;
                    }

                    item.color = (item.team == 2 ? "#f33" : "#33f");
                    var arc = ctx.display.arc({
                        x: item.x,
                        y: item.y,
                        radius: 7,
                        start: 0,
                        end: 360,
                        fill: item.color
                    });

                    arc.item = item;
                    arc.visible = true;

                    ctx.addChild(arc);

                    if (item.what == 2) {
                        arc.bind('mouseenter', function (e) {
                            this.fill = "#eee";
                            ctx.redraw();

                            $("#tooltip").html(this.item.entype).css({
                                top: e.pageY - 30,
                                left: e.pageX,
                            }).show();

                        });

                        arc.bind('mouseleave', function (e) {
                            this.fill = this.item.color;
                            ctx.redraw();
                            $("#tooltip").hide();
                        });

                        state.structures.push(arc);
                    } else if (item.what == 1) {
                        state.kills.push(arc);
                    }
                }
                state.maxvalue = Math.round((state.newest - state.oldest) / this.state.diff);
                state.value = state.maxvalue;
                state.timetable = this.timeTable(state.value);
                this.setState(state);
            }
        }.bind(this));
    }
});
