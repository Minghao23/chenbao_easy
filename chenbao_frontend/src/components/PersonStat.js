import React, {Component} from 'react';
import ReactEcharts from 'echarts-for-react';
import {message, Layout, Row, Col} from 'antd';
import {ChartCard} from 'ant-design-pro/lib/Charts'
import "antd/dist/antd.css";
import "ant-design-pro/dist/ant-design-pro.css";
import moment from "moment";
import StatForm from "./StatForm";
import {MyHeader, MyFooter} from "./MyLayout"
import {host, port} from "./config"

export default class PersonStat extends Component {
    constructor(props) {
        super(props);
        this.req_host = host;
        this.req_port = port;

        this.state = this.getInitialState();
        this.getStaffs();
    }

    getInitialState = () => ({
        staffs: [],
        dates: [],
        send_times: [],
        you_diff: '',
        total_average: '',
        earliest_person: '',
        earliest_diff: '',
        latest_person: '',
        latest_diff: '',
    });

    // ----------------
    // |   Requests   |
    // ----------------

    getStaffs() {
        let endpoint = 'init';
        fetch('http://' + this.req_host + ':' + this.req_port + '/' + endpoint, {
            method: 'GET'
        }).then(res => res.json()).then(
            data => {
                this.setState({
                    staffs: data.staffs,
                });
            }
        ).catch((err) => message.error("Server error!", err))
    }

    personStat(payload) {
        let endpoint = 'person_stat';
        fetch('http://' + this.req_host + ':' + this.req_port + '/' + endpoint, {
            method: 'POST',
            body: JSON.stringify(payload)
        }).then(res => res.json()).then(
            data => {
                let temp_send_times = [];
                let temp_dates = [];
                for (let i = 0; i < data.date.length; i++) {
                    let cur_time_value = moment(data.time[i], 'HH:mm:ss');
                    temp_dates.push(moment(data.date[i], "YYYYMMDD").format("YYYY-MM-DD"));
                    temp_send_times.push(
                        cur_time_value.hour() * 60 * 60 +
                        cur_time_value.minute() * 60 +
                        cur_time_value.second()
                    );
                }
                this.setState({
                    dates: temp_dates,
                    send_times: temp_send_times,
                    you_diff: data.you_diff,
                    total_average: data.total_average,
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

    handleFormSubmit = (inputs) => {
        const payload = {
            // 'name': inputs.name,
            'name': inputs.name,
            'start_date': inputs.start_date,
            'end_date': inputs.end_date
        };
        this.personStat(payload);
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
            return `发报日期：${index}<br/>当天未发晨报`;
        }
        let hour = Math.floor(value / 3600);
        let minute = Math.floor((value % 3600) / 60);
        let second = value % 60;
        let label = moment([2019, 1, 1, hour, minute, second]).format('HH:mm:ss');
        return `发报日期：${index}<br/>发报时间：${label}`;
    };

    timeValueMarklineFormat = (params) => {
        let value = params.data.value;
        let hour = Math.floor(value / 3600);
        let minute = Math.floor((value % 3600) / 60);
        let second = value % 60;
        return moment([2019, 1, 1, hour, minute, second]).format('HH:mm:ss');
    };

    colorTimeDiff = (diff) => {
        if (diff[0] === '早') {
            return <span style={{color: "green"}}>{diff}</span>
        } else if (diff[0] === '晚') {
            return <span style={{color: "red"}}>{diff}</span>
        } else {
            return <span style={{color: "blue"}}>{diff}</span>
        }
    };

    getOption = () => ({
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
                data: this.state.send_times,
                markLine: {
                    data: [
                        {
                            type: 'average',
                            name: '平均发报时间',
                        }
                    ],
                    label: {
                        formatter: this.timeValueMarklineFormat
                    }
                }
            },
        ],
    });

    render() {

        const {Content} = Layout;

        return (
            <Layout className="layout">
                <MyHeader/>
                <Content className="content">
                    <div>
                        <h1 className="page_title">个人发报时间统计</h1>
                        <div className='stat_form_area'>
                            <br/>
                            <StatForm staffs={this.state.staffs} handler={this.handleFormSubmit}/>
                            <br/>
                        </div>
                        <div>
                            <Row>
                                <Col span={8} style={{padding: 20}}>
                                    <ChartCard
                                        title="全体员工平均发报时间"
                                        total={this.state.total_average}
                                        footer={
                                            <div>
                                                <span>您的发报时间比平均时间</span>
                                                <br/>
                                                {this.colorTimeDiff(this.state.you_diff)}
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
                        <div className='chart_area'>
                            <ReactEcharts  option={this.getOption()} style={{height: 400}}/>
                        </div>
                    </div>
                </Content>
                <MyFooter/>
            </Layout>
        );
    }
}
