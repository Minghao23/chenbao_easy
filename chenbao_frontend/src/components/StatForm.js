import React, {Component} from 'react';
import {Form, DatePicker, Button, Input, message} from 'antd';
import moment from "moment";

export default class StatForm extends Component {
    constructor(props) {
        super(props);

        this.state = this.getInitialState();
    }

    getInitialState = () => ({
        name: '',
        start_date: moment().add(-10, 'days').format("YYYYMMDD"),
        end_date: moment().format("YYYYMMDD"),
    });

    handlerSubmit = () => {
        this.props.handler(this.state)
    };

    handleEnterKey = (e) => {
        if (e.which !== 13) return;
        if (this.props.staffs.indexOf(this.state.name) === -1) {
            message.error('该员工姓名不存在！');
            return
        }
        this.handlerSubmit()
    };

    handleConfirmButton = (e) => {
        if (!this.props.dropname && this.props.staffs.indexOf(this.state.name) === -1) {
            message.error('该员工姓名不存在！');
            return
        }
        this.handlerSubmit()
    };

    handleNameChange = (e) => {
        this.setState({
            name: e.target.value
        });
    };

    handleRangePicker = (date, dateString) => {
        this.setState({
            start_date: date[0].format("YYYYMMDD"),
            end_date: date[1].format("YYYYMMDD"),
        });
    };

    disabledDate = (current) => {
        return current > moment().endOf('day');
    };

    getNameInput = () => {
        if (this.props.dropname) {
            return null
        } else {
            return <Form.Item label="姓名">
                <Input
                    type="text"
                    size="default"
                    onChange={this.handleNameChange}
                    onKeyPress={this.handleEnterKey}
                />
            </Form.Item>
        }
    };

    render() {
        const {RangePicker} = DatePicker;

        return (
            <Form layout="inline">
                {this.getNameInput()}
                <Form.Item label="日期">
                    <RangePicker
                        defaultValue={[
                            moment(this.state.start_date, 'YYYYMMDD'),
                            moment(this.state.end_date, 'YYYYMMDD')
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
                </Form.Item>
                <Form.Item>
                    <div className="button_area">
                        <Button type="primary"
                                size="default"
                                onClick={this.handleConfirmButton}
                        >确认</Button>
                    </div>
                </Form.Item>
            </Form>
        );
    }
}

