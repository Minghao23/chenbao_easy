import React, {Component} from 'react';
import ReactEcharts from 'echarts-for-react';
import {message, Layout, DatePicker, Button} from 'antd';
import "antd/dist/antd.css";
import moment from "moment";
import {MyHeader, MyFooter} from "./MyLayout"
import {host, port} from "./config"

export default class TotalStat extends Component {
    constructor(props) {
        super(props);
        this.req_host = host;
        this.req_port = port;

        this.init_start_date = moment().add(-10, 'days');
        this.init_end_date = moment();

        this.state = this.getInitialState();
    }

    getInitialState = () => ({
        dates: [],
        send_persons: [],
        absent_persons: [],
    });

    // ----------------
    // |   Requests   |
    // ----------------

    totalStat(payload) {
        let endpoint = 'total_stat';
        fetch('http://' + this.req_host + ':' + this.req_port + '/' + endpoint, {
            method: 'POST',
            body: JSON.stringify(payload)
        }).then(res => res.json()).then(
            data => {
                let temp_send_persons = [];
                let temp_absent_persons = [];
                let temp_dates = [];
                for (let i = 0; i < data.date.length; i++) {
                    temp_dates.push(moment(data.date[i], "YYYYMMDD").format("YYYY-MM-DD"));
                    temp_send_persons.push(data.sent_cb_person[i]);
                    temp_absent_persons.push(data.absent_person[i]);
                }
                this.setState({
                    dates: temp_dates,
                    send_persons: temp_send_persons,
                    absent_persons: temp_absent_persons,
                });
            }
        ).catch((err) => message.error("Server error!", err))
    }

    // ----------------
    // |   Handlers   |
    // ----------------

    componentDidMount() {
        const payload = {
            'start_date': this.init_start_date.format("YYYYMMDD"),
            'end_date': this.init_end_date.format("YYYYMMDD"),
        };
        this.totalStat(payload);
    }

    handleRangePicker = (date, dateString) => {
        const payload = {
            'start_date': date[0].format("YYYYMMDD"),
            'end_date': date[1].format("YYYYMMDD"),
        };
        this.totalStat(payload);
    };

    disabledDate = (current) => {
        return current > moment().endOf('day');
    };

    getDatePickerShortCut = (shortcut) => {
        let tmp_start_date = this.init_start_date;
        let tmp_end_date = this.init_end_date;

        if (shortcut === '本周') {
            tmp_start_date = moment().startOf('week');
            tmp_end_date = moment().endOf('week');
        } else if (shortcut === '本月') {
            tmp_start_date = moment().startOf('month');
            tmp_end_date = moment().endOf('month');
        } else if (shortcut === '本季度') {
            tmp_start_date = moment().startOf('quarter');
            tmp_end_date = moment().endOf('quarter');
        }

        return <Button className="shortcut_button" type="ghost" onClick={(e) => {
            const payload = {
                'start_date': tmp_start_date.format("YYYYMMDD"),
                'end_date': tmp_end_date.format("YYYYMMDD"),
            };
            this.totalStat(payload);
        }}>
            {shortcut}
        </Button>
    };

    getOption = () => ({
        tooltip: {
            trigger: 'axis',
        },
        legend: {
            data: ['发报人数', '请假人数']
        },
        xAxis: {
            type: 'category',
            name: '日期',
            data: this.state.dates
        },
        yAxis: {
            type: 'value',
            name: '人数',
        },
        series: [
            {
                name: '发报人数',
                type: 'bar',
                stack: '总人数',
                data: this.state.send_persons,
            },
            {
                name: '请假人数',
                type: 'bar',
                stack: '总人数',
                data: this.state.absent_persons,
            },
        ],
        color: [
            '#1890ff',
            '#2f4554'
        ]
    });

    render() {

        const {RangePicker} = DatePicker;

        const {Content} = Layout;

        return (
            <Layout className="layout">
                <MyHeader/>
                <Content className="content">
                    <div>
                        <h1 className="page_title">全局统计</h1>
                        <div className='stat_form_area'>
                            <RangePicker
                                defaultValue={[
                                    this.init_start_date,
                                    this.init_end_date
                                ]}
                                disabledDate={this.disabledDate}
                                ranges={{
                                    Today: [moment(), moment()],
                                    'This Month': [moment().startOf('month'), moment().endOf('month')],
                                    'Last 10 Days': [moment().add(-10, 'days'), moment()],
                                    'Last 3 Months': [moment().add(-3, 'months'), moment()],
                                    'Last Year': [moment().add(-1, 'year'), moment()],
                                }}
                                onChange={this.handleRangePicker}
                                allowClear={false}/>
                            {this.getDatePickerShortCut('本周')}
                            {this.getDatePickerShortCut('本月')}
                            {this.getDatePickerShortCut('本季度')}
                        </div>
                        <br/>
                        <div className='chart_area'>
                            <ReactEcharts option={this.getOption()} style={{height: 400}}/>
                        </div>
                    </div>
                </Content>
                <MyFooter/>
            </Layout>
        );
    }
}
