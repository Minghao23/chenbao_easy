(window.webpackJsonp=window.webpackJsonp||[]).push([[0],{1010:function(e,t,a){"use strict";a.r(t);var n=a(0),r=a.n(n),l=a(9),s=a.n(l),o=(a(452),a(46)),i=a(47),c=a(49),m=a(48),u=a(50),h=(a(453),a(117)),d=a(97),f=a(1021),p=a(1022),_=a(444),E=a(1019),b=a(1017),g=a(116),y=a(12),v=a(445),S=a(1023),C=a(42),Y=a(1012),O=a(1013),k=a(1020),M=(a(167),a(289)),D=f.a.Header,N=f.a.Footer,j=f.a.Sider,T=function(e){function t(e){var a;return Object(o.a)(this,t),(a=Object(c.a)(this,Object(m.a)(t).call(this,e))).onCollapse=function(e){a.setState({collapsed:e})},a.state={collapsed:!0},a}return Object(u.a)(t,e),Object(i.a)(t,[{key:"render",value:function(){return r.a.createElement(j,{collapsible:!0,collapsed:this.state.collapsed,onCollapse:this.onCollapse},r.a.createElement(M.a,{defaultSelectedKeys:["1"],mode:"inline",theme:"dark",inlineCollapsed:this.state.collapsed},r.a.createElement(M.a.Item,{key:"1"},r.a.createElement(h.b,{to:"/"},r.a.createElement(y.a,{type:"home"}),r.a.createElement("span",null,"\u4e3b\u9875"))),r.a.createElement(M.a.Item,{key:"2"},r.a.createElement(h.b,{to:"/PersonHistory"},r.a.createElement(y.a,{type:"file-search"}),r.a.createElement("span",null,"\u5386\u53f2\u67e5\u8be2"))),r.a.createElement(M.a.Item,{key:"3"},r.a.createElement(h.b,{to:"/PersonStat"},r.a.createElement(y.a,{type:"line-chart"}),r.a.createElement("span",null,"\u4e2a\u4eba\u6570\u636e"))),r.a.createElement(M.a.Item,{key:"4"},r.a.createElement(h.b,{to:"/TotalStat"},r.a.createElement(y.a,{type:"pie-chart"}),r.a.createElement("span",null,"\u5168\u5c40\u7edf\u8ba1")))))}}]),t}(n.Component),x=function(){return r.a.createElement(D,{className:"header"},r.a.createElement(y.a,{type:"schedule",theme:"filled"}),"\xa0\xa0\xa0",r.a.createElement("span",{className:"title"},r.a.createElement("b",null,"\u6668\u62a5\u6613")),"\xa0\xa0\xa0",r.a.createElement("span",{className:"subtitle"},"\u6668\u62a5\u5904\u7406\u66f4\u5bb9\u6613"))},I=function(){return r.a.createElement(N,{style:{textAlign:"center"}},"Created by ",r.a.createElement("a",{href:"https://www.minghao23.com",target:"_blank",rel:"noopener noreferrer"},"Minghao Hu")," \xa92019")},P="localhost",w="8012",q=function(e){function t(e){var a;return Object(o.a)(this,t),(a=Object(c.a)(this,Object(m.a)(t).call(this,e))).getInitialState=function(){return{staffs:[],remaining_persons:["\u70b9\u51fb '\u8fd8\u6709\u8c01\uff01'\uff0c\u770b\u770b\u5230\u5e95\u662f\u8c01\u8fd8\u6ca1\u53d1\u6668\u62a5\uff01"],absent_persons:[],tag_input_visible:!1,tag_input_value:"",data_source:[],chat_content:"",popconfirm_visible:!1,modal_visible:!1,modal_loading:!1,email_to:"",email_cc:"",email_subject:"",email_message:""}},a.handleCloseTag=function(e,t){e.preventDefault();var n=a.state.absent_persons.filter(function(e){return e!==t});a.setState({absent_persons:n}),a.updateAbsentPersons(n)},a.showTagInput=function(e){a.setState({tag_input_visible:!0}),e.target.focus()},a.handleSearch=function(e){var t=a.state.staffs.filter(function(t){return-1===a.state.absent_persons.indexOf(t)&&t.indexOf(e)>=0});a.setState({data_source:t})},a.handleSelect=function(e){var t=a.state.absent_persons;t.push(e),a.setState({absent_persons:t,tag_input_visible:!1}),a.updateAbsentPersons(t)},a.handleTagInputCancel=function(){a.setState({tag_input_visible:!1})},a.handleContentChange=function(e){a.setState({chat_content:e.target.value})},a.handleCheckButton=function(){var e={chat_content:a.state.chat_content,absent_persons:a.state.absent_persons};a.checkContent(e)},a.handleGenerateButton=function(){var e={chat_content:a.state.chat_content,absent_persons:a.state.absent_persons};a.generateEmail(e),a.handleShowModal()},a.handleShowModal=function(){a.setState({modal_visible:!0})},a.handleModalSendEmail=function(){a.setState({modal_loading:!0}),setTimeout(function(){a.setState({modal_loading:!1}),p.a.success("\u5df2\u53d1\u9001")},2e3),setTimeout(function(){p.a.error("\u54c8\u54c8\u54c8\u9a97\u4f60\u7684\uff01")},5e3),setTimeout(function(){p.a.error("\u8be5\u529f\u80fd\u9884\u8ba1\u4e8ev2.0\u7248\u672c\u4e0a\u7ebf")},8e3)},a.handleModalReturn=function(){a.setState({modal_visible:!1})},a.handleEmailToChange=function(e){a.setState({email_to:e.target.value})},a.handleEmailCcChange=function(e){a.setState({email_cc:e.target.value})},a.handleEmailSubjectChange=function(e){a.setState({email_subject:e.target.value})},a.handleEmailMessageChange=function(e){a.setState({email_message:e.target.value})},a.handlePopConfirmConfirm=function(){a.setState({popconfirm_visible:!1}),a.handleGenerateButton()},a.handlePopConfirmCancel=function(){a.setState({popconfirm_visible:!1})},a.handlePopConfirmVisibleChange=function(e){if(e){var t={chat_content:a.state.chat_content,absent_persons:a.state.absent_persons};a.beforeGenerateEmail(t)}else a.setState({popconfirm_visible:e})},a.handleClearIcon=function(){a.setState({chat_content:""})},a.req_host=P,a.req_port=w,a.state=a.getInitialState(),a.getData(),a}return Object(u.a)(t,e),Object(i.a)(t,[{key:"getData",value:function(){var e=this;fetch("http://"+this.req_host+":"+this.req_port+"/init",{method:"GET"}).then(function(e){return e.json()}).then(function(t){e.setState({staffs:t.staffs,absent_persons:t.absent_persons})}).catch(function(e){return p.a.error("Server error!",e)})}},{key:"updateAbsentPersons",value:function(e){fetch("http://"+this.req_host+":"+this.req_port+"/update",{method:"POST",body:JSON.stringify({absent_persons:e})}).catch(function(e){return p.a.error("Server error!",e)})}},{key:"checkContent",value:function(e){var t=this;fetch("http://"+this.req_host+":"+this.req_port+"/check",{method:"POST",body:JSON.stringify(e)}).then(function(e){return e.json()}).then(function(e){t.setState({remaining_persons:e.remaining_persons})}).catch(function(e){return p.a.error("Server error!",e)})}},{key:"generateEmail",value:function(e){var t=this;fetch("http://"+this.req_host+":"+this.req_port+"/generate",{method:"POST",body:JSON.stringify(e)}).then(function(e){return e.json()}).then(function(e){t.setState({email_to:e.to,email_cc:e.cc,email_subject:e.subject,email_message:e.message})}).catch(function(e){return p.a.error("Server error!",e)})}},{key:"beforeGenerateEmail",value:function(e){var t=this;fetch("http://"+this.req_host+":"+this.req_port+"/check",{method:"POST",body:JSON.stringify(e)}).then(function(e){return e.json()}).then(function(e){t.setState({remaining_persons:e.remaining_persons})}).then(function(){t.state.remaining_persons.length<=0?(t.handlePopConfirmConfirm(),p.a.info("\u4e0d\u53ef\u601d\u8bae\uff01\u6240\u6709\u4eba\u90fd\u53d1\u4e86\u6668\u62a5\uff01")):t.setState({popconfirm_visible:!0})}).catch(function(e){return p.a.error("Server error!",e)})}},{key:"render",value:function(){var e=this,t=_.a.TextArea,a=E.a.Text,n=f.a.Content;return r.a.createElement(f.a,{className:"layout"},r.a.createElement(x,null),r.a.createElement(n,{className:"content"},r.a.createElement("div",null,r.a.createElement("div",{className:"form_area"},r.a.createElement(b.a.Item,null,r.a.createElement("h1",{className:"label"},r.a.createElement(g.a,{placement:"bottomLeft",style:{width:"300px"},title:r.a.createElement("span",null,"\u4ee5\u59d3\u540d\u5f00\u5934\u7684QQ\u6d88\u606f\u88ab\u8ba4\u4e3a\u662f\u6709\u6548\u7684\u6668\u62a5",r.a.createElement("br",null),"\u590d\u5236\u65f6\u8bf7\u5c3d\u91cf\u907f\u514d\u9057\u6f0f\u5185\u5bb9")},r.a.createElement("span",null,r.a.createElement(y.a,{type:"file-text"}),"\xa0\xa0\u804a\u5929\u8bb0\u5f55"))),r.a.createElement("label",null,"\u5728\u8fd9\u91cc\u590d\u5236\u6668\u62a5\u7fa4\u91cc\u4eca\u5929\u6240\u6709\u7684QQ\u804a\u5929\u8bb0\u5f55\uff0c\u6668\u62a5\u6613\u4f1a\u81ea\u52a8\u68c0\u6d4b\u548c\u53bb\u9664\u65e0\u5173\u5185\u5bb9\uff0c\u91cd\u65b0\u6392\u7248\u5e76\u751f\u6210\u90ae\u4ef6"),r.a.createElement("div",{className:"clear_icon_area"},r.a.createElement(y.a,{onClick:this.handleClearIcon,type:"delete"})),r.a.createElement(t,{rows:10,placeholder:"Content in QQ group",style:{resize:"none"},value:this.state.chat_content,onChange:this.handleContentChange})),r.a.createElement(b.a.Item,null,r.a.createElement("h1",{className:"label"},r.a.createElement(g.a,{placement:"bottomLeft",title:"\u5bf9\u8bf7\u5047\u4eba\u5458\u7684\u4fee\u6539\u5c06\u4f1a\u88ab\u4fdd\u5b58"},r.a.createElement("span",null,r.a.createElement(y.a,{type:"user"}),"\xa0\xa0\u8bf7\u5047\u4eba\u5458"))),this.state.absent_persons.map(function(t){return r.a.createElement(v.a,{key:t,color:"red",closable:!0,onClose:function(a){e.handleCloseTag(a,t)}},t)}),this.state.tag_input_visible&&r.a.createElement(S.a,{dataSource:this.state.data_source,style:{width:100},onSelect:this.handleSelect,onSearch:this.handleSearch,onBlur:this.handleTagInputCancel,placeholder:"Name",autoFocus:!0}),!this.state.tag_input_visible&&r.a.createElement(v.a,{color:"red",onClick:this.showTagInput,style:{background:"#fff",borderStyle:"dashed"}},r.a.createElement(y.a,{type:"plus"})," Person")),r.a.createElement("br",null),r.a.createElement(b.a.Item,null,r.a.createElement("div",{className:"button_area"},r.a.createElement(C.a,{type:"default",size:"large",onClick:this.handleCheckButton},"\u8fd8\u6709\u8c01\uff01"),r.a.createElement(Y.a,{title:"\u4ecd\u6709"+this.state.remaining_persons.length+"\u4eba\u672a\u53d1\u6668\u62a5\uff0c\u662f\u5426\u7ee7\u7eed\u751f\u6210\u90ae\u4ef6\uff1f",visible:this.state.popconfirm_visible,onVisibleChange:this.handlePopConfirmVisibleChange,onConfirm:this.handlePopConfirmConfirm,onCancel:this.handlePopConfirmCancel,okText:"\u7ee7\u7eed",cancelText:"\u53d6\u6d88"},r.a.createElement(C.a,{type:"primary",size:"large"},"\u751f\u6210\u90ae\u4ef6")))),r.a.createElement("br",null)),r.a.createElement("div",{className:"alert_area"},r.a.createElement(O.a,{className:"alert",message:"\u672a\u53d1\u6668\u62a5",type:"info",showIcon:!0,description:r.a.createElement("div",null,r.a.createElement("br",null),r.a.createElement("p",null,this.state.remaining_persons.map(function(e){return e+" "})),r.a.createElement("p",null,r.a.createElement(a,{copyable:{text:this.state.remaining_persons.map(function(e){return"@"+e})+"\uff08QQ\u76ee\u524d\u4e0d\u652f\u6301\u62f7\u8d1d@\u64cd\u4f5c\uff0c\u4ecd\u9700\u8981\u624b\u52a8@\uff09"}},"\uff08\u590d\u5236\u5230QQ\uff09")))})),r.a.createElement(k.a,{width:"60%",className:"modal",visible:this.state.modal_visible,title:"\u5317\u4eac\u6668\u62a5\u90ae\u4ef6",onOk:this.handleModalSendEmail,onCancel:this.handleModalReturn,footer:[r.a.createElement(C.a,{key:"back",onClick:this.handleModalReturn},"\u8fd4\u56de"),r.a.createElement(C.a,{key:"submit",type:"primary",loading:this.state.modal_loading,onClick:this.handleModalSendEmail},"\u53d1\u9001\u90ae\u4ef6")],closable:!1,keyboard:!1,maskClosable:!1,destroyOnClose:!0},r.a.createElement(b.a,{labelCol:{span:4},wrapperCol:{span:16}},r.a.createElement(b.a.Item,{label:"\u6536\u4ef6\u4eba"},r.a.createElement(_.a,{value:this.state.email_to,onChange:this.handleEmailToChange,suffix:r.a.createElement(a,{copyable:{text:this.state.email_to}})})),r.a.createElement(b.a.Item,{label:"\u6284\u9001"},r.a.createElement(_.a,{value:this.state.email_cc,onChange:this.handleEmailCcChange,suffix:r.a.createElement(a,{copyable:{text:this.state.email_cc}})})),r.a.createElement(b.a.Item,{label:"\u4e3b\u9898"},r.a.createElement(_.a,{value:this.state.email_subject,onChange:this.handleEmailSubjectChange,suffix:r.a.createElement(a,{copyable:{text:this.state.email_subject}})})),r.a.createElement(b.a.Item,{label:"\u6b63\u6587"},r.a.createElement(t,{style:{resize:"none"},rows:10,value:this.state.email_message,onChange:this.handleEmailMessageChange})))))),r.a.createElement(I,null))}}]),t}(n.Component),H=a(1016),L=a(10),V=a.n(L),F=a(1018),B=function(e){function t(e){var a;return Object(o.a)(this,t),(a=Object(c.a)(this,Object(m.a)(t).call(this,e))).getInitialState=function(){return{name:"",start_date:V()().add(-10,"days").format("YYYYMMDD"),end_date:V()().format("YYYYMMDD")}},a.handlerSubmit=function(){a.props.handler(a.state)},a.handleEnterKey=function(e){13===e.which&&(-1!==a.props.staffs.indexOf(a.state.name)?a.handlerSubmit():p.a.error("\u8be5\u5458\u5de5\u59d3\u540d\u4e0d\u5b58\u5728\uff01"))},a.handleConfirmButton=function(e){a.props.dropname||-1!==a.props.staffs.indexOf(a.state.name)?a.handlerSubmit():p.a.error("\u8be5\u5458\u5de5\u59d3\u540d\u4e0d\u5b58\u5728\uff01")},a.handleNameChange=function(e){a.setState({name:e.target.value})},a.handleRangePicker=function(e,t){a.setState({start_date:e[0].format("YYYYMMDD"),end_date:e[1].format("YYYYMMDD")})},a.disabledDate=function(e){return e>V()().endOf("day")},a.getNameInput=function(){return a.props.dropname?null:r.a.createElement(b.a.Item,{label:"\u59d3\u540d"},r.a.createElement(_.a,{type:"text",size:"default",onChange:a.handleNameChange,onKeyPress:a.handleEnterKey}))},a.state=a.getInitialState(),a}return Object(u.a)(t,e),Object(i.a)(t,[{key:"render",value:function(){var e=F.a.RangePicker;return r.a.createElement(b.a,{layout:"inline"},this.getNameInput(),r.a.createElement(b.a.Item,{label:"\u65e5\u671f"},r.a.createElement(e,{defaultValue:[V()(this.state.start_date,"YYYYMMDD"),V()(this.state.end_date,"YYYYMMDD")],disabledDate:this.disabledDate,ranges:{Today:[V()(),V()()],"This Month":[V()().startOf("month"),V()().endOf("month")],"Last 10 Days":[V()().add(-10,"days"),V()()],"Last 3 Months":[V()().add(-3,"months"),V()()],"Last Year":[V()().add(-1,"year"),V()()]},onChange:this.handleRangePicker,allowClear:!1})),r.a.createElement(b.a.Item,null,r.a.createElement("div",{className:"button_area"},r.a.createElement(C.a,{type:"primary",size:"default",onClick:this.handleConfirmButton},"\u786e\u8ba4"))))}}]),t}(n.Component),A=function(e){function t(e){var a;return Object(o.a)(this,t),(a=Object(c.a)(this,Object(m.a)(t).call(this,e))).getInitialState=function(){return{staffs:[],history:[]}},a.handleFormSubmit=function(e){var t={name:e.name,start_date:e.start_date,end_date:e.end_date};a.personHistory(t)},a.req_host=P,a.req_port=w,a.state=a.getInitialState(),a.getStaffs(),a}return Object(u.a)(t,e),Object(i.a)(t,[{key:"getStaffs",value:function(){var e=this;fetch("http://"+this.req_host+":"+this.req_port+"/init",{method:"GET"}).then(function(e){return e.json()}).then(function(t){e.setState({staffs:t.staffs})}).catch(function(e){return p.a.error("Server error!",e)})}},{key:"personHistory",value:function(e){var t=this;fetch("http://"+this.req_host+":"+this.req_port+"/person_history",{method:"POST",body:JSON.stringify(e)}).then(function(e){return e.json()}).then(function(e){for(var a=[],n=0;n<e.date.length;n++)a.push({key:n+1,date:e.date[n],content:e.content[n]});t.setState({history:a})}).catch(function(e){return p.a.error("Server error!",e)})}},{key:"render",value:function(){var e=[{title:"\u65e5\u671f",dataIndex:"date",key:"date",render:function(e){return V()(e.toString(),"YYYYMMDD").format("YYYY\u5e74MM\u6708DD\u65e5")}},{title:"\u6668\u62a5\u5185\u5bb9",dataIndex:"content",key:"content",render:function(e,t){if(null==e)return e;for(var a=e.toString().split("\n"),n=null,l=0;l<a.length;l++)n=0===l?a[l]:r.a.createElement("span",null,n,r.a.createElement("br",null),a[l]);return r.a.createElement("div",null,n)}}],t=f.a.Content;return r.a.createElement(f.a,{className:"layout"},r.a.createElement(x,null),r.a.createElement(t,{className:"content"},r.a.createElement("div",null,r.a.createElement("h1",{className:"page_title"},"\u5386\u53f2\u6668\u62a5\u67e5\u8be2"),r.a.createElement("div",{className:"stat_form_area"},r.a.createElement("br",null),r.a.createElement(B,{staffs:this.state.staffs,handler:this.handleFormSubmit}),r.a.createElement("br",null)),r.a.createElement("div",{className:"table_area"},r.a.createElement(H.a,{dataSource:this.state.history,columns:e,pagination:{pageSize:15}})))),r.a.createElement(I,null))}}]),t}(n.Component),R=a(165),Q=a.n(R),J=a(1014),z=a(1015),G=a(120),K=(a(1009),function(e){function t(e){var a;return Object(o.a)(this,t),(a=Object(c.a)(this,Object(m.a)(t).call(this,e))).getInitialState=function(){return{staffs:[],dates:[],send_times:[],total_avg:"",your_avg:"",you_diff:"",beyond_percentage:""}},a.handleFormSubmit=function(e){var t={name:e.name,start_date:e.start_date,end_date:e.end_date};a.personStat(t)},a.timeValueLabelFormat=function(e,t){var a=Math.floor(e/3600),n=Math.floor(e%3600/60);return V()([2019,1,1,a,n]).format("HH:mm")},a.timeValueTooltipFormat=function(e){var t=e[0].axisValue,a=e[0].data;if(isNaN(a))return"\u53d1\u62a5\u65e5\u671f\uff1a".concat(t,"<br/>\u5f53\u5929\u672a\u53d1\u6668\u62a5");var n=Math.floor(a/3600),r=Math.floor(a%3600/60),l=a%60,s=V()([2019,1,1,n,r,l]).format("HH:mm:ss");return"\u53d1\u62a5\u65e5\u671f\uff1a".concat(t,"<br/>\u53d1\u62a5\u65f6\u95f4\uff1a").concat(s)},a.timeValueMarklineFormat=function(e){var t=e.data.value,a=Math.floor(t/3600),n=Math.floor(t%3600/60),r=t%60;return V()([2019,1,1,a,n,r]).format("HH:mm:ss")},a.colorTimeDiff=function(e){return null===e?"":"\u65e9"===e[0]?r.a.createElement("span",{style:{color:"green"}},e):"\u665a"===e[0]?r.a.createElement("span",{style:{color:"red"}},e):r.a.createElement("span",{style:{color:"blue"}},e)},a.getPercentReply=function(e){return null===e||""===e?r.a.createElement("br",null):parseInt(e)>=50?"\u4fdd\u6301\u4f4f\uff01\u4e0d\u8981\u5fd8\u4e86\u5728\u6668\u62a5\u4e2d\u5199\u660e bug \u5904\u7406\u60c5\u51b5\u54e6\uff01":0===parseInt(e)?"\u539f\u6765\u4f60\u5c31\u662f\u90a3\u4e2a\u6700\u540e\u4e00\u4e2a\u53d1\u6668\u62a5\u7684\uff01":"\u4f60\u6668\u62a5\u53d1\u7684\u592a\u665a\u4e86\uff01\u4e89\u53d6\u6210\u4e3a\u524d 50% \u5148\uff01\u52a0\u6cb9\uff01"},a.getOption=function(){return{tooltip:{trigger:"axis",formatter:a.timeValueTooltipFormat},xAxis:{type:"category",name:"\u65e5\u671f",data:a.state.dates},yAxis:{type:"value",inverse:!0,min:0,max:86400,splitNumber:8,name:"\u65f6\u95f4",axisLabel:{formatter:a.timeValueLabelFormat}},series:[{name:"\u53d1\u62a5\u65f6\u95f4",type:"line",itemStyle:{normal:{color:"#177CB0"}},data:a.state.send_times,markLine:{data:[{type:"average",name:"\u5e73\u5747\u53d1\u62a5\u65f6\u95f4"}],label:{formatter:a.timeValueMarklineFormat}}}]}},a.req_host=P,a.req_port=w,a.state=a.getInitialState(),a.getStaffs(),a}return Object(u.a)(t,e),Object(i.a)(t,[{key:"getStaffs",value:function(){var e=this;fetch("http://"+this.req_host+":"+this.req_port+"/init",{method:"GET"}).then(function(e){return e.json()}).then(function(t){e.setState({staffs:t.staffs})}).catch(function(e){return p.a.error("Server error!",e)})}},{key:"personStat",value:function(e){var t=this;fetch("http://"+this.req_host+":"+this.req_port+"/person_stat",{method:"POST",body:JSON.stringify(e)}).then(function(e){return e.json()}).then(function(e){for(var a=[],n=[],r=0;r<e.date.length;r++){var l=V()(e.time[r],"HH:mm:ss");n.push(V()(e.date[r],"YYYYMMDD").format("YYYY-MM-DD")),a.push(60*l.hour()*60+60*l.minute()+l.second())}t.setState({dates:n,send_times:a,total_avg:e.total_avg,your_avg:e.your_avg,you_diff:e.you_diff,beyond_percentage:e.beyond_percentage})}).catch(function(e){return p.a.error("Server error!",e)})}},{key:"render",value:function(){var e=f.a.Content;return r.a.createElement(f.a,{className:"layout"},r.a.createElement(x,null),r.a.createElement(e,{className:"content"},r.a.createElement("div",null,r.a.createElement("h1",{className:"page_title"},"\u4e2a\u4eba\u53d1\u62a5\u65f6\u95f4\u7edf\u8ba1"),r.a.createElement("div",{className:"stat_form_area"},r.a.createElement("br",null),r.a.createElement(B,{staffs:this.state.staffs,handler:this.handleFormSubmit}),r.a.createElement("br",null)),r.a.createElement("div",{className:"card_area"},r.a.createElement(J.a,null,r.a.createElement(z.a,{span:12,style:{padding:20}},r.a.createElement(G.ChartCard,{title:"\u4f60\u7684\u5e73\u5747\u53d1\u62a5\u65f6\u95f4",total:this.state.your_avg,footer:r.a.createElement("div",null,r.a.createElement("span",null,"\u6bd4\u603b\u4f53\u5e73\u5747\u65f6\u95f4"),this.colorTimeDiff(this.state.you_diff)),contentHeight:46})),r.a.createElement(z.a,{span:12,style:{padding:20}},r.a.createElement(G.ChartCard,{title:"\u8d85\u8fc7\u7684\u5458\u5de5\u6bd4\u4f8b",total:this.state.beyond_percentage,footer:r.a.createElement("div",null,this.getPercentReply(this.state.beyond_percentage)),contentHeight:46})))),r.a.createElement("br",null),r.a.createElement("div",{className:"chart_area"},r.a.createElement("h3",{className:"page_title subtitle"},"\u4e2a\u4eba\u53d1\u62a5\u65f6\u95f4\u66f2\u7ebf"),r.a.createElement(Q.a,{option:this.getOption(),style:{height:400}})))),r.a.createElement(I,null))}}]),t}(n.Component)),W=a(287),$=a.n(W),U=function(e){function t(e){var a;return Object(o.a)(this,t),(a=Object(c.a)(this,Object(m.a)(t).call(this,e))).getInitialState=function(){return{dates:[],send_persons:[],absent_persons:[],avg_send_time:[],total_avg:"",trend:"",earliest_person:"",earliest_diff:"",latest_person:"",latest_diff:""}},a.handleRangePicker=function(e,t){var n={start_date:e[0].format("YYYYMMDD"),end_date:e[1].format("YYYYMMDD")};a.totalStat(n)},a.disabledDate=function(e){return e>V()().endOf("day")},a.colorTimeDiff=function(e){return null===e?"":"\u65e9"===e[0]?r.a.createElement("span",{style:{color:"green"}},e):"\u665a"===e[0]?r.a.createElement("span",{style:{color:"red"}},e):r.a.createElement("span",{style:{color:"blue"}},e)},a.colorTrend=function(e){return"\u4e0a"===e[0]?r.a.createElement("span",{style:{color:"green"}}," ",e,r.a.createElement($.a,{flag:"up"})):"\u4e0b"===e[0]?r.a.createElement("span",{style:{color:"red"}},e,r.a.createElement($.a,{flag:"down"})):r.a.createElement("span",{style:{color:"blue"}},e)},a.getDatePickerShortCut=function(e){var t=a.init_start_date,n=a.init_end_date;return"\u672c\u5468"===e?(t=V()().startOf("week"),n=V()().endOf("week")):"\u672c\u6708"===e?(t=V()().startOf("month"),n=V()().endOf("month")):"\u672c\u5b63\u5ea6"===e&&(t=V()().startOf("quarter"),n=V()().endOf("quarter")),r.a.createElement(C.a,{className:"shortcut_button",type:"ghost",onClick:function(e){var r={start_date:t.format("YYYYMMDD"),end_date:n.format("YYYYMMDD")};a.totalStat(r)}},e)},a.timeValueLabelFormat=function(e,t){var a=Math.floor(e/3600),n=Math.floor(e%3600/60);return V()([2019,1,1,a,n]).format("HH:mm")},a.timeValueTooltipFormat=function(e){var t=e[0].axisValue,a=e[0].data;if(isNaN(a))return"\u53d1\u62a5\u65e5\u671f\uff1a".concat(t,"<br/>\u672a\u8bb0\u5f55");var n=Math.floor(a/3600),r=Math.floor(a%3600/60),l=a%60,s=V()([2019,1,1,n,r,l]).format("HH:mm:ss");return"\u53d1\u62a5\u65e5\u671f\uff1a".concat(t,"<br/>\u5e73\u5747\u53d1\u62a5\u65f6\u95f4\uff1a").concat(s)},a.getBarOption=function(){return{tooltip:{trigger:"axis"},legend:{data:["\u53d1\u62a5\u4eba\u6570","\u8bf7\u5047\u4eba\u6570"]},xAxis:{type:"category",name:"\u65e5\u671f",data:a.state.dates},yAxis:{type:"value",name:"\u4eba\u6570"},series:[{name:"\u53d1\u62a5\u4eba\u6570",type:"bar",stack:"\u603b\u4eba\u6570",data:a.state.send_persons},{name:"\u8bf7\u5047\u4eba\u6570",type:"bar",stack:"\u603b\u4eba\u6570",data:a.state.absent_persons}],color:["#1890ff","#2f4554"]}},a.getLineOption=function(){return{tooltip:{trigger:"axis",formatter:a.timeValueTooltipFormat},xAxis:{type:"category",name:"\u65e5\u671f",data:a.state.dates},yAxis:{type:"value",inverse:!0,min:0,max:86400,splitNumber:8,name:"\u65f6\u95f4",axisLabel:{formatter:a.timeValueLabelFormat}},series:[{name:"\u53d1\u62a5\u65f6\u95f4",type:"line",itemStyle:{normal:{color:"#177CB0"}},data:a.state.avg_send_time}]}},a.req_host=P,a.req_port=w,a.init_start_date=V()().add(-10,"days"),a.init_end_date=V()(),a.state=a.getInitialState(),a}return Object(u.a)(t,e),Object(i.a)(t,[{key:"totalStat",value:function(e){var t=this;fetch("http://"+this.req_host+":"+this.req_port+"/total_stat",{method:"POST",body:JSON.stringify(e)}).then(function(e){return e.json()}).then(function(e){for(var a=[],n=[],r=[],l=[],s=0;s<e.date.length;s++){var o=V()(e.avg_send_time[s],"HH:mm:ss");l.push(60*o.hour()*60+60*o.minute()+o.second()),r.push(V()(e.date[s],"YYYYMMDD").format("YYYY-MM-DD")),a.push(e.sent_cb_person[s]),n.push(e.absent_person[s])}t.setState({dates:r,send_persons:a,absent_persons:n,avg_send_time:l,total_avg:e.total_avg,trend:e.trend,earliest_person:e.earliest_person,earliest_diff:e.earliest_diff,latest_person:e.latest_person,latest_diff:e.latest_diff})}).catch(function(e){return p.a.error("Server error!",e)})}},{key:"componentDidMount",value:function(){var e={start_date:this.init_start_date.format("YYYYMMDD"),end_date:this.init_end_date.format("YYYYMMDD")};this.totalStat(e)}},{key:"render",value:function(){var e=F.a.RangePicker,t=f.a.Content;return r.a.createElement(f.a,{className:"layout"},r.a.createElement(x,null),r.a.createElement(t,{className:"content"},r.a.createElement("div",null,r.a.createElement("h1",{className:"page_title"},"\u5168\u5c40\u7edf\u8ba1"),r.a.createElement("div",{className:"stat_form_area"},r.a.createElement(e,{defaultValue:[this.init_start_date,this.init_end_date],disabledDate:this.disabledDate,ranges:{Today:[V()(),V()()],"This Month":[V()().startOf("month"),V()().endOf("month")],"Last 10 Days":[V()().add(-10,"days"),V()()],"Last 3 Months":[V()().add(-3,"months"),V()()],"Last Year":[V()().add(-1,"year"),V()()]},onChange:this.handleRangePicker,allowClear:!1}),this.getDatePickerShortCut("\u672c\u5468"),this.getDatePickerShortCut("\u672c\u6708"),this.getDatePickerShortCut("\u672c\u5b63\u5ea6")),r.a.createElement("br",null),r.a.createElement("div",{className:"card_area"},r.a.createElement(J.a,null,r.a.createElement(z.a,{span:8,style:{padding:20}},r.a.createElement(G.ChartCard,{title:"\u5168\u4f53\u5458\u5de5\u5e73\u5747\u53d1\u62a5\u65f6\u95f4",total:this.state.total_avg,footer:r.a.createElement("div",null,r.a.createElement("span",null,"\u4e8e\u672c\u5468\u671f\u5185\u5448"),r.a.createElement("br",null),this.colorTrend(this.state.trend)),contentHeight:46})),r.a.createElement(z.a,{span:8,style:{padding:20}},r.a.createElement(G.ChartCard,{title:"\u65e5\u5747\u53d1\u62a5\u65f6\u95f4\u6700\u65e9\u5458\u5de5",total:this.state.earliest_person,footer:r.a.createElement("div",null,r.a.createElement("span",null,"\u6bd4\u5e73\u5747\u65f6\u95f4"),r.a.createElement("br",null),this.colorTimeDiff(this.state.earliest_diff)),contentHeight:46})),r.a.createElement(z.a,{span:8,style:{padding:20}},r.a.createElement(G.ChartCard,{title:"\u65e5\u5747\u53d1\u62a5\u65f6\u95f4\u6700\u665a\u5458\u5de5",total:this.state.latest_person,footer:r.a.createElement("div",null,r.a.createElement("span",null,"\u6bd4\u5e73\u5747\u65f6\u95f4"),r.a.createElement("br",null),this.colorTimeDiff(this.state.latest_diff)),contentHeight:46})))),r.a.createElement("br",null),r.a.createElement("div",{className:"chart_area"},r.a.createElement("h3",{className:"page_title subtitle"},"\u6bcf\u65e5\u6668\u62a5\u53d1\u9001\u7edf\u8ba1"),r.a.createElement(Q.a,{option:this.getBarOption(),style:{height:400}})),r.a.createElement("br",null),r.a.createElement("div",{className:"chart_area"},r.a.createElement("h3",{className:"page_title subtitle"},"\u6bcf\u65e5\u53d1\u62a5\u5e73\u5747\u65f6\u95f4\u66f2\u7ebf"),r.a.createElement(Q.a,{option:this.getLineOption(),style:{height:400}})))),r.a.createElement(I,null))}}]),t}(n.Component),X=function(e){function t(){return Object(o.a)(this,t),Object(c.a)(this,Object(m.a)(t).apply(this,arguments))}return Object(u.a)(t,e),Object(i.a)(t,[{key:"render",value:function(){return r.a.createElement(f.a,{style:{minHeight:"100vh"}},r.a.createElement(h.a,null,r.a.createElement(T,null),r.a.createElement(d.a,{exact:!0,path:"/",component:q}),r.a.createElement(d.a,{path:"/PersonHistory",component:A}),r.a.createElement(d.a,{path:"/PersonStat",component:K}),r.a.createElement(d.a,{path:"/TotalStat",component:U})))}}]),t}(n.Component);Boolean("localhost"===window.location.hostname||"[::1]"===window.location.hostname||window.location.hostname.match(/^127(?:\.(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)){3}$/));s.a.render(r.a.createElement(X,null),document.getElementById("root")),"serviceWorker"in navigator&&navigator.serviceWorker.ready.then(function(e){e.unregister()})},447:function(e,t,a){e.exports=a(1010)},452:function(e,t,a){},453:function(e,t,a){}},[[447,1,2]]]);
//# sourceMappingURL=main.9353db0c.chunk.js.map