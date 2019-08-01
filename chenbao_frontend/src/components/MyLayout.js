import React, {Component} from 'react';
import {Icon, Layout, Menu} from "antd";
import {Link} from 'react-router-dom'

const {Header, Footer, Sider} = Layout;

export class MySider extends Component {

    constructor(props) {
        super(props);

        this.state = {
            collapsed: true,
        };
    }

    onCollapse = collapsed => {
        this.setState({collapsed});
    };

    render() {
        return (
            <Sider collapsible collapsed={this.state.collapsed} onCollapse={this.onCollapse}>
                <Menu
                    defaultSelectedKeys={['1']}
                    mode="inline"
                    theme="dark"
                    inlineCollapsed={this.state.collapsed}
                >
                    <Menu.Item key="1">
                        <Link to="/">
                            <Icon type="home"/>
                            <span>主页</span>
                        </Link>
                    </Menu.Item>
                    <Menu.Item key="2">
                        <Link to="/PersonHistory">
                            <Icon type="file-search"/>
                            <span>历史查询</span>
                        </Link>
                    </Menu.Item>
                    <Menu.Item key="3">
                        <Link to="/PersonStat">
                            <Icon type="line-chart"/>
                            <span>个人数据</span>
                        </Link>
                    </Menu.Item>
                    <Menu.Item key="4">
                        <Link to="/TotalStat">
                            <Icon type="pie-chart"/>
                            <span>全局统计</span>
                        </Link>
                    </Menu.Item>
                </Menu>
            </Sider>
        )
    }
}


export const MyHeader = () =>
    <Header className='header'>
        <Icon type="schedule" theme="filled"/>
        &nbsp;&nbsp;&nbsp;
        <span className='title'><b>晨报易</b></span>
        &nbsp;&nbsp;&nbsp;
        <span className='subtitle'>晨报处理更容易</span>
    </Header>;


export const MyFooter = () =>
    <Footer style={{textAlign: 'center'}}>
        Created by <a href={"https://www.minghao23.com"} target="_blank" rel="noopener noreferrer">Minghao Hu</a> ©2019
    </Footer>;

