import React, {Component} from 'react';
import {Table, message, Layout} from 'antd';
import "antd/dist/antd.css";
import moment from "moment";
import StatForm from "./StatForm";
import {MyHeader, MyFooter} from "./MyLayout"
import {host, port} from "./config"

export default class PersonHistory extends Component {
    constructor(props) {
        super(props);
        this.req_host = host;
        this.req_port = port;

        this.state = this.getInitialState();
        this.getStaffs();
    }

    getInitialState = () => ({
        staffs: [],
        history: [],
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

    personHistory(payload) {
        let endpoint = 'person_history';
        fetch('http://' + this.req_host + ':' + this.req_port + '/' + endpoint, {
            method: 'POST',
            body: JSON.stringify(payload)
        }).then(res => res.json()).then(
            data => {
                let historys = [];
                for (let i = 0; i < data.date.length; i++) {
                    historys.push({
                        key: i + 1,
                        date: data.date[i],
                        content: data.content[i],
                    })
                }
                this.setState({
                    history: historys,
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
        this.personHistory(payload);
    };

    render() {
        const columns = [
            {
                title: '日期',
                dataIndex: 'date',
                key: 'date',
                render: text => (moment(text.toString(), "YYYYMMDD").format("YYYY年MM月DD日"))
            },
            {
                title: '晨报内容',
                dataIndex: 'content',
                key: 'content',
                render: (text, record) => {  // handle change line problem
                    if (text == null) return text;
                    let text_split = text.toString().split('\n');
                    let result = null;
                    for (let i = 0; i < text_split.length; i++) {
                        if (i === 0) {
                            result = text_split[i]
                        } else {
                            result = <span>{result}<br/>{text_split[i]}</span>
                        }
                    }
                    return <div>{result}</div>
                },
            },
        ];

        const {Content} = Layout;

        return (
            <Layout className="layout">
                <MyHeader/>
                <Content className="content">
                    <div>
                        <h1 className="page_title">历史晨报查询</h1>
                        <div className='stat_form_area'>
                            <br/>
                            <StatForm staffs={this.state.staffs} handler={this.handleFormSubmit}/>
                            <br/>
                        </div>
                        <div className='table_area'>
                            <Table dataSource={this.state.history}
                                   columns={columns}
                                   pagination={{pageSize: 15}}/>
                        </div>
                    </div>
                </Content>
                <MyFooter/>
            </Layout>
        );
    }
}