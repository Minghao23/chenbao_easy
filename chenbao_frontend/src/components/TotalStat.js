import React, {Component} from 'react';
import ReactEcharts from 'echarts-for-react';
import {message, Layout, DatePicker, Button, Row, Col} from 'antd';
import {ChartCard} from 'ant-design-pro/lib/Charts'
import Trend from 'ant-design-pro/lib/Trend';
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
        avg_send_time: [],
        total_avg: '',
        trend: '',
        earliest_person: '',
        earliest_diff: '',
        latest_person: '',
        latest_diff: '',
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
                let temp_avg_send_time = [];
                for (let i = 0; i < data.date.length; i++) {
                    let cur_time_value = moment(data.avg_send_time[i], 'HH:mm:ss');
                    temp_avg_send_time.push(
                        cur_time_value.hour() * 60 * 60 +
                        cur_time_value.minute() * 60 +
                        cur_time_value.second()
                    );
                    temp_dates.push(moment(data.date[i], "YYYYMMDD").format("YYYY-MM-DD"));
                    temp_send_persons.push(data.sent_cb_person[i]);
                    temp_absent_persons.push(data.absent_person[i]);
                }
                this.setState({
                    dates: temp_dates,
                    send_persons: temp_send_persons,
                    absent_persons: temp_absent_persons,
                    avg_send_time: temp_avg_send_time,
                    total_avg: data.total_avg,
                    trend: data.trend,
                    earliest_person: data.earliest_person,
                    earliest_diff: data.earliest_diff,
                    latest_person: data.latest_person,
                    latest_diff: data.latest_diff,
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

    colorTimeDiff = (diff) => {
        if (diff === null) {
            return ''
        }
        if (diff[0] === '早') {
            return <span style={{color: "green"}}>{diff}</span>
        } else if (diff[0] === '晚') {
            return <span style={{color: "red"}}>{diff}</span>
        } else {
            return <span style={{color: "blue"}}>{diff}</span>
        }
    };

    colorTrend = (trend) => {
        if (trend[0] === '上') {
            return <span style={{color: "green"}}> {trend}<Trend flag="up" /></span>
        } else if (trend[0] === '下') {
            return <span style={{color: "red"}}>{trend}<Trend flag="down" /></span>
        } else {
            return <span style={{color: "blue"}}>{trend}</span>
        }
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

    timeValueLabelFormat = (value, index) => {
        let hour = Math.floor(value / 3600);
        let minute = Math.floor((value % 3600) / 60);
        return moment([2019, 1, 1, hour, minute]).format('HH:mm');
    };

    timeValueTooltipFormat = (params) => {
        let index = params[0].axisValue;
        let value = params[0].data;
        if (isNaN(value)) {
            return `发报日期：${index}<br/>未记录`;
        }
        let hour = Math.floor(value / 3600);
        let minute = Math.floor((value % 3600) / 60);
        let second = value % 60;
        let label = moment([2019, 1, 1, hour, minute, second]).format('HH:mm:ss');
        return `发报日期：${index}<br/>平均发报时间：${label}`;
    };

    getBarOption = () => ({
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

    getLineOption = () => ({
        tooltip: {
            trigger: 'axis',
            formatter: this.timeValueTooltipFormat
        },
        xAxis: {
            type: 'category',
            name: '日期',
            data: this.state.dates
        },
        yAxis: {
            type: 'value',
            inverse: true,
            min: 0,
            max: 24 * 60 * 60,
            splitNumber: 8,
            name: '时间',
            axisLabel: {
                formatter: this.timeValueLabelFormat
            }
        },
        series: [
            {
                name: '发报时间',
                type: 'line',
                itemStyle: {
                    normal: {
                        color: '#177CB0'
                    }
                },
                data: this.state.avg_send_time,
            },
        ],
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
                        <div className="card_area">
                            <Row>
                                <Col span={8} style={{padding: 20}}>
                                    <ChartCard
                                        title="全体员工平均发报时间"
                                        total={this.state.total_avg}
                                        footer={
                                            <div>
                                                <span>于本周期内呈</span>
                                                <br/>
                                                {this.colorTrend(this.state.trend)}
                                            </div>}
                                        contentHeight={46}
                                    />
                                </Col>
                                <Col span={8} style={{padding: 20}}>
                                    <ChartCard
                                        title="日均发报时间最早员工"
                                        total={this.state.earliest_person}
                                        footer={
                                            <div>
                                                <span>比平均时间</span>
                                                <br/>
                                                {this.colorTimeDiff(this.state.earliest_diff)}
                                            </div>}
                                        contentHeight={46}
                                    />
                                </Col>
                                <Col span={8} style={{padding: 20}}>
                                    <ChartCard
                                        title="日均发报时间最晚员工"
                                        total={this.state.latest_person}
                                        footer={
                                            <div>
                                                <span>比平均时间</span>
                                                <br/>
                                                {this.colorTimeDiff(this.state.latest_diff)}
                                            </div>}
                                        contentHeight={46}
                                    />
                                </Col>
                            </Row>
                        </div>
                        <br/>
                        <div className='chart_area'>
                            <h3 className="page_title subtitle">每日晨报发送统计</h3>
                            <ReactEcharts option={this.getBarOption()} style={{height: 400}}/>
                        </div>
                        <br/>
                        <div className='chart_area'>
                            <h3 className="page_title subtitle">每日发报平均时间曲线</h3>
                            <ReactEcharts  option={this.getLineOption()} style={{height: 400}}/>
                        </div>
                    </div>
                </Content>
                <MyFooter/>
            </Layout>
        );
    }
}
