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
        total_avg: '',
        your_avg: '',
        you_diff: '',
        beyond_percentage: '',
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
                    total_avg: data.total_avg,
                    your_avg: data.your_avg,
                    you_diff: data.you_diff,
                    beyond_percentage: data.beyond_percentage,
                });
            }
        ).catch((err) => message.error("Server error!", err))
    }

    // ----------------
    // |   Handlers   |
    // ----------------

    handleFormSubmit = (inputs) => {
        const payload = {
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

    getPercentReply = (percentage) => {
        if (percentage === null || percentage === '') {
            return <br/>
        }
        if (parseInt(percentage) >= 50) {
            return '保持住！不要忘了在晨报中写明 bug 处理情况哦！'
        } else if (parseInt(percentage) === 0) {
            return '原来你就是那个最后一个发晨报的！'
        } else {
            return '你晨报发的太晚了！争取成为前 50% 先！加油！'
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
                        <div className="card_area">
                            <Row>
                                <Col span={12} style={{padding: 20}}>
                                    <ChartCard
                                        title="你的平均发报时间"
                                        total={this.state.your_avg}
                                        footer={
                                            <div>
                                                <span>比总体平均时间</span>
                                                {this.colorTimeDiff(this.state.you_diff)}
                                            </div>}
                                        contentHeight={46}
                                    />
                                </Col>
                                <Col span={12} style={{padding: 20}}>
                                    <ChartCard
                                        title="超过的员工比例"
                                        total={this.state.beyond_percentage}
                                        footer={
                                            <div>
                                                {this.getPercentReply(this.state.beyond_percentage)}
                                            </div>}
                                        contentHeight={46}
                                    />
                                </Col>
                            </Row>
                        </div>
                        <br/>
                        <div className='chart_area'>
                            <h3 className="page_title subtitle">个人发报时间曲线</h3>
                            <ReactEcharts  option={this.getOption()} style={{height: 400}}/>
                        </div>
                    </div>
                </Content>
                <MyFooter/>
            </Layout>
        );
    }
}
