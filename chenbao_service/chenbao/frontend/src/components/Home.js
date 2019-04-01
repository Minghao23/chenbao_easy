import React, {Component} from 'react';
import {  message, Tooltip, Layout, Typography, Popconfirm, Modal, AutoComplete, Tag, Alert, Icon, Button, Form, Input} from 'antd';
import "antd/dist/antd.css";

export default class Home extends Component {
    constructor(props) {
        super(props);
        this.req_host = '127.0.0.1';
        this.req_port = '8012';

        this.state = this.getInitialState();
        this.getData();
    }

    getInitialState = () => ({
        staffs: [],
        remaining_persons: ["点击 '还有谁！'，看看到底是谁还没发晨报！"],
        absent_persons: [],
        tag_input_visible: false,
        tag_input_value: '',
        data_source: [],
        chat_content: '',
        popconfirm_visible: false,

        modal_visible: false,
        modal_loading: false,
        email_to: '',
        email_cc: '',
        email_subject: '',
        email_message: '',
    });

    // ----------------
    // |   Requests   |
    // ----------------

    getData() {
        let endpoint = 'init';
        fetch('http://' + this.req_host + ':' + this.req_port + '/' + endpoint,{
            method: 'GET'
        }).then(res => res.json()).then(
            data => {
                this.setState({
                    staffs: data.staffs,
                    absent_persons: data.absent_persons
                });
            }
        ).catch((err) =>message.error("Server error!", err))
    }

    updateAbsentPersons(cur_absent_persons) {
        let endpoint = 'update';
        fetch('http://' + this.req_host + ':' + this.req_port + '/' + endpoint,{
            method: 'POST',
            body: JSON.stringify({'absent_persons': cur_absent_persons})
        }).catch((err) =>message.error("Server error!", err))
    }

    checkContent(payload) {
        let endpoint = 'check';
        fetch('http://' + this.req_host + ':' + this.req_port + '/' + endpoint,{
            method: 'POST',
            body: JSON.stringify(payload)
        }).then(res => res.json()).then(
            data => {
                this.setState({
                    remaining_persons: data.remaining_persons
                });
            }
        ).catch((err) =>message.error("Server error!", err))
    }

    generateEmail(payload) {
        let endpoint = 'generate';
        fetch('http://' + this.req_host + ':' + this.req_port + '/' + endpoint,{
            method: 'POST',
            body: JSON.stringify(payload)
        }).then(res => res.json()).then(
            data => {
                this.setState({
                    email_to: data.to,
                    email_cc: data.cc,
                    email_subject: data.subject,
                    email_message: data.message,
                });
            }
        ).catch((err) =>message.error("Server error!", err))
    }

    beforeGenerateEmail(payload) {
        let endpoint = 'check';
        fetch('http://' + this.req_host + ':' + this.req_port + '/' + endpoint,{
            method: 'POST',
            body: JSON.stringify(payload)
        }).then(res => res.json()).then(
            data => {
                this.setState({
                    remaining_persons: data.remaining_persons
                });
            }
        ).then(
            () => {
                if (this.state.remaining_persons.length <= 0) {
                    this.handlePopConfirmConfirm();
                    message.info("不可思议！所有人都发了晨报！")
                } else {
                    this.setState({ popconfirm_visible: true });
                }
            }
        ).catch((err) =>message.error("Server error!", err))
    }

    // ----------------
    // |   Handlers   |
    // ----------------

    handleCloseTag = (e, name) => {
        e.preventDefault();  // must prevent the original close animation ... why??
        const new_absent_persons = this.state.absent_persons.filter(absent_person => absent_person !== name);
        this.setState({
            absent_persons: new_absent_persons
        });
        this.updateAbsentPersons(new_absent_persons);
    };

    showTagInput = (e) => {
        this.setState({
            tag_input_visible: true
        });
        e.target.focus();
    };

    handleSearch = (value) => {
        const new_data_source = this.state.staffs.filter(name =>
            this.state.absent_persons.indexOf(name) === -1 && name.indexOf(value) >= 0);
        this.setState({
            data_source: new_data_source
        });
    };

    handleSelect = (value) => {
        const new_absent_persons = this.state.absent_persons;
        new_absent_persons.push(value);
        this.setState({
            absent_persons: new_absent_persons,
            tag_input_visible: false
        });
        this.updateAbsentPersons(new_absent_persons);
    };

    handleTagInputCancel = () => {
        this.setState({
            tag_input_visible: false
        });
    };

    handleContentChange = (e) => {
        this.setState({
            chat_content: e.target.value
        });
    };

    handleCheckButton = () => {
        const payload = {
            'chat_content': this.state.chat_content,
            'absent_persons': this.state.absent_persons};
        this.checkContent(payload);
    };

    handleGenerateButton = () => {
        const payload = {
            'chat_content': this.state.chat_content,
            'absent_persons': this.state.absent_persons};
        this.generateEmail(payload);
        this.handleShowModal();
    };

    handleShowModal = () => {
        this.setState({
            modal_visible: true,
        });
    };

    handleModalSendEmail = () => {
        // TODO Really send email
        this.setState({ modal_loading: true });
        setTimeout(() => {
            this.setState({
                modal_loading: false
            });
            message.success("已发送");
        }, 2000);
        setTimeout(() => {
            message.error("假的，愚人节快乐！");
        }, 5000);
        setTimeout(() => {
            message.error("该功能预计于v2.0版本上线")
        }, 8000);
    };

    handleModalReturn = () => {
        this.setState({ modal_visible: false });
    };

    handleEmailToChange = (e) => {
        this.setState({
            email_to: e.target.value
        });
    };

    handleEmailCcChange = (e) => {
        this.setState({
            email_cc: e.target.value
        });
    };

    handleEmailSubjectChange = (e) => {
        this.setState({
            email_subject: e.target.value
        });
    };

    handleEmailMessageChange = (e) => {
        this.setState({
            email_message: e.target.value
        });
    };

    handlePopConfirmConfirm = () => {
        this.setState({ popconfirm_visible: false });
        this.handleGenerateButton();
    };

    handlePopConfirmCancel = () => {
        this.setState({ popconfirm_visible: false });
    };

    handlePopConfirmVisibleChange = (visible) => {
        if (!visible) {
            this.setState({ popconfirm_visible: visible });
            return;
        }
        const payload = {
            'chat_content': this.state.chat_content,
            'absent_persons': this.state.absent_persons
        };
        this.beforeGenerateEmail(payload);  // must set visible after check remaining persons
    };

    handleClearIcon = () => {
        this.setState({
            chat_content: ''
        });
    };

    render() {

        const { TextArea } = Input;

        const { Text } = Typography;

        const { Header, Content, Footer } = Layout;

        return (
            <Layout className="layout">
                <Header className='header'>
                    <Icon type="schedule" theme="filled" />
                    &nbsp;&nbsp;&nbsp;
                    <span className='title'><b>晨报易</b></span>
                    &nbsp;&nbsp;&nbsp;
                    <span className='subtitle'>晨报处理更容易</span>
                </Header>
                <Content className="content">
                    <div>
                        <div className='form_area'>
                            <Form.Item>
                                <h1 className="label">
                                    <Tooltip placement="bottomLeft" style={{ width: "300px" }} title={<span>以姓名开头的QQ消息被认为是有效的晨报<br/>复制时请尽量避免遗漏内容</span>}>
                                        <span><Icon type="file-text" />&nbsp;&nbsp;聊天记录</span>
                                    </Tooltip>
                                </h1>
                                <label>在这里复制晨报群里今天所有的QQ聊天记录，晨报易会自动检测和去除无关内容，重新排版并生成邮件</label>
                                <div className="clear_icon_area"><Icon onClick={this.handleClearIcon} type="delete" /></div>
                                <TextArea rows={10} placeholder="Content in QQ group" style={{ resize: 'none' }}
                                          value={this.state.chat_content}
                                          onChange={this.handleContentChange}/>
                            </Form.Item>
                            <Form.Item>
                                <h1 className="label">
                                    <Tooltip placement="bottomLeft" title="对请假人员的修改将会被保存">
                                        <span><Icon type="user" />&nbsp;&nbsp;请假人员</span>
                                    </Tooltip>
                                </h1>
                                {this.state.absent_persons.map((person) => {
                                    return <Tag key={person} color="red" closable
                                                onClose={(e)=>{this.handleCloseTag(e, person)}}>{person}</Tag>
                                })}
                                {this.state.tag_input_visible && (
                                    <AutoComplete
                                        dataSource={this.state.data_source}
                                        style={{ width: 100 }}
                                        onSelect={this.handleSelect}
                                        onSearch={this.handleSearch}
                                        onBlur={this.handleTagInputCancel}
                                        placeholder="Name"
                                        autoFocus
                                    />
                                )}
                                {!this.state.tag_input_visible && (
                                    <Tag
                                        color="red"
                                        onClick={this.showTagInput}
                                        style={{ background: '#fff', borderStyle: 'dashed' }}
                                    >
                                        <Icon type="plus" /> Person
                                    </Tag>
                                )}
                            </Form.Item>
                            <br/>
                            <Form.Item>
                                <div className="button_area">
                                    <Button type="default" size="large" onClick={this.handleCheckButton}>还有谁！</Button>
                                    <Popconfirm title={"仍有" + this.state.remaining_persons.length + "人未发晨报，是否继续生成邮件？"}
                                                visible={this.state.popconfirm_visible}
                                                onVisibleChange={this.handlePopConfirmVisibleChange}
                                                onConfirm={this.handlePopConfirmConfirm}
                                                onCancel={this.handlePopConfirmCancel}
                                                okText="继续"
                                                cancelText="取消">
                                        <Button type="primary" size="large">生成邮件</Button>
                                    </Popconfirm>
                                </div>
                            </Form.Item>
                            <br/>
                        </div>
                        <div className='alert_area'>
                            <Alert className='alert' message='未发晨报' type="info" showIcon
                                   description={
                                       <div>
                                           <br/>
                                           <p>{this.state.remaining_persons.map(
                                               (person) => person + ' ')}</p>
                                           <p><Text copyable={{
                                               text: this.state.remaining_persons.map((person) => '@' + person)
                                           }}>（复制到QQ）</Text></p>
                                       </div>
                                   }/>
                        </div>

                        <Modal
                            width="60%"
                            className="modal"
                            visible={this.state.modal_visible}
                            title="北京晨报邮件"
                            onOk={this.handleModalSendEmail}
                            onCancel={this.handleModalReturn}
                            footer={[
                                <Button key="back" onClick={this.handleModalReturn}>返回</Button>,
                                <Button key="submit" type="primary" loading={this.state.modal_loading} onClick={this.handleModalSendEmail}>
                                    发送邮件
                                </Button>
                            ]}
                            closable={false}
                            keyboard={false}
                            maskClosable={false}
                            destroyOnClose
                        >
                            <Form labelCol={{ span: 4 }} wrapperCol={{ span: 16 }}>
                                <Form.Item label="收件人">
                                    <Input value={this.state.email_to} onChange={this.handleEmailToChange}
                                           suffix={<Text copyable={{ text: this.state.email_to }}/>}/>
                                </Form.Item>
                                <Form.Item label="抄送">
                                    <Input value={this.state.email_cc} onChange={this.handleEmailCcChange}
                                           suffix={<Text copyable={{ text: this.state.email_cc }}/>}/>
                                </Form.Item>
                                <Form.Item label="主题">
                                    <Input value={this.state.email_subject} onChange={this.handleEmailSubjectChange}
                                           suffix={<Text copyable={{ text: this.state.email_subject }}/>}/>
                                </Form.Item>
                                <Form.Item label="正文">
                                    <TextArea style={{ resize: 'none' }}
                                              rows={10}
                                              value={this.state.email_message}
                                              onChange={this.handleEmailMessageChange}
                                    />
                                    <Text copyable={{ text: this.state.email_message }}/>
                                </Form.Item>
                            </Form>
                        </Modal>
                    </div>
                </Content>
                <Footer style={{ textAlign: 'center' }}>
                    Created by <a href={"https://www.minghao23.com"} target="_blank" rel="noopener noreferrer">Minghao Hu</a> ©2019
                </Footer>
            </Layout>
        );
    }
}