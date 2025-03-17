document.addEventListener('DOMContentLoaded', function() {
    // 获取DOM元素
    const introSection = document.getElementById('intro-section');
    const questionnaireSection = document.getElementById('questionnaire-section');
    const loadingSection = document.getElementById('loading-section');
    const reportSection = document.getElementById('report-section');
    
    const startBtn = document.getElementById('start-btn');
    const prevBtn = document.getElementById('prev-btn');
    const nextBtn = document.getElementById('next-btn');
    const submitBtn = document.getElementById('submit-btn');
    const downloadBtn = document.getElementById('download-btn');
    const restartBtn = document.getElementById('restart-btn');
    
    const questionGroups = document.querySelectorAll('.question-group');
    const form = document.getElementById('questionnaire-form');
    const reportContent = document.getElementById('report-content');
    const reportTime = document.getElementById('report-time');
    
    // 当前问题索引
    let currentQuestionIndex = 0;
    
    // 开始按钮点击事件
    startBtn.addEventListener('click', function() {
        introSection.classList.add('hidden');
        questionnaireSection.classList.remove('hidden');
        showQuestion(0);
    });
    
    // 显示特定问题
    function showQuestion(index) {
        // 隐藏所有问题
        questionGroups.forEach(group => {
            group.classList.remove('active');
        });
        
        // 显示当前问题
        questionGroups[index].classList.add('active');
        
        // 更新按钮状态
        prevBtn.disabled = index === 0;
        
        if (index === questionGroups.length - 1) {
            nextBtn.classList.add('hidden');
            submitBtn.classList.remove('hidden');
        } else {
            nextBtn.classList.remove('hidden');
            submitBtn.classList.add('hidden');
        }
        
        currentQuestionIndex = index;
    }
    
    // 上一题按钮点击事件
    prevBtn.addEventListener('click', function() {
        if (currentQuestionIndex > 0) {
            showQuestion(currentQuestionIndex - 1);
        }
    });
    
    // 下一题按钮点击事件
    nextBtn.addEventListener('click', function() {
        const currentTextarea = questionGroups[currentQuestionIndex].querySelector('textarea');
        
        // 简单验证（可选）
        if (currentTextarea.value.trim() === '') {
            if (!confirm('此问题尚未回答，确定要继续吗？')) {
                return;
            }
        }
        
        if (currentQuestionIndex < questionGroups.length - 1) {
            showQuestion(currentQuestionIndex + 1);
        }
    });
    
    // 表单提交事件
    form.addEventListener('submit', function(e) {
        e.preventDefault();
        
        // 收集所有回答
        const answers = {};
        questionGroups.forEach(group => {
            const questionId = group.dataset.questionId;
            const textarea = group.querySelector('textarea');
            answers[questionId] = textarea.value.trim();
        });
        
        // 获取学生姓名
        const studentName = document.getElementById('student-name').value.trim() || '同学';
        
        // 显示加载界面
        questionnaireSection.classList.add('hidden');
        loadingSection.classList.remove('hidden');
        
        // 发送请求到后端
        fetch('/generate', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                answers: answers,
                name: studentName
            }),
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                // 显示报告
                loadingSection.classList.add('hidden');
                reportSection.classList.remove('hidden');
                
                // 格式化报告内容
                const formattedReport = formatReport(data.report, studentName);
                reportContent.innerHTML = formattedReport;
                
                // 设置报告时间
                reportTime.textContent = data.timestamp;
            } else {
                // 显示错误
                alert('生成报告时出错：' + data.error);
                loadingSection.classList.add('hidden');
                questionnaireSection.classList.remove('hidden');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('发生错误，请重试');
            loadingSection.classList.add('hidden');
            questionnaireSection.classList.remove('hidden');
        });
    });
    
    // 格式化报告内容
    function formatReport(report, name) {
        // 添加学生姓名
        let formattedReport = `<h3>亲爱的 ${name}：</h3>`;
        
        // 将报告文本转换为HTML格式
        // 分段落
        const paragraphs = report.split('\n\n');
        
        paragraphs.forEach(paragraph => {
            // 处理标题
            if (paragraph.startsWith('#')) {
                const level = paragraph.match(/^#+/)[0].length;
                const title = paragraph.replace(/^#+\s*/, '');
                formattedReport += `<h${level + 2}>${title}</h${level + 2}>`;
            } 
            // 处理列表
            else if (paragraph.includes('\n- ')) {
                const listItems = paragraph.split('\n- ');
                const title = listItems.shift();
                
                if (title) {
                    formattedReport += `<p>${title}</p>`;
                }
                
                formattedReport += '<ul>';
                listItems.forEach(item => {
                    formattedReport += `<li>${item}</li>`;
                });
                formattedReport += '</ul>';
            } 
            // 普通段落
            else if (paragraph.trim()) {
                formattedReport += `<p>${paragraph}</p>`;
            }
        });
        
        return formattedReport;
    }
    
    // 下载报告
    downloadBtn.addEventListener('click', function() {
        const studentName = document.getElementById('student-name').value.trim() || '同学';
        const timestamp = reportTime.textContent;
        
        // 创建 PDF 文档
        const { jsPDF } = window.jspdf;
        const doc = new jsPDF({
            orientation: 'portrait',
            unit: 'mm',
            format: 'a4',
        });
        
        // 设置中文字体
        doc.setFont('helvetica');
        doc.setFontSize(16);
        
        // 添加标题
        doc.setTextColor(228, 70, 47);
        doc.text('学生个人品牌顾问报告', 105, 20, { align: 'center' });
        
        // 添加基本信息
        doc.setFontSize(12);
        doc.setTextColor(0, 0, 0);
        doc.text(`生成时间：${timestamp}`, 20, 30);
        doc.text(`学生姓名：${studentName}`, 20, 40);
        
        // 使用 html2canvas 将报告内容转换为图像
        html2canvas(reportContent, {
            scale: 2,
            useCORS: true,
            logging: false,
            allowTaint: true
        }).then(canvas => {
            // 将画布转换为图像
            const imgData = canvas.toDataURL('image/jpeg', 0.8);
            
            // 计算适当的图像大小
            const imgWidth = 170; // A4 纸宽度的可用区域
            const pageHeight = 297;  // A4 高度
            const imgHeight = canvas.height * imgWidth / canvas.width;
            let heightLeft = imgHeight;
            let position = 50; // 起始位置
            
            // 添加第一页图像
            doc.addImage(imgData, 'JPEG', 20, position, imgWidth, imgHeight);
            heightLeft -= (pageHeight - position);
            
            // 如果内容超过一页，添加新页
            while (heightLeft >= 0) {
                position = 0;
                doc.addPage();
                doc.addImage(imgData, 'JPEG', 20, position - (imgHeight - heightLeft), imgWidth, imgHeight);
                heightLeft -= pageHeight;
            }
            
            // 添加页脚
            const pageCount = doc.internal.getNumberOfPages();
            for (let i = 1; i <= pageCount; i++) {
                doc.setPage(i);
                doc.setFontSize(10);
                doc.setTextColor(100, 100, 100);
                doc.text(`基于Llama 3开源模型 | 第 ${i} 页 / 共 ${pageCount} 页`, 105, 287, { align: 'center' });
            }
            
            // 保存 PDF
            doc.save(`个人品牌报告_${studentName}_${new Date().toISOString().slice(0, 10)}.pdf`);
        });
    });
    
    // 重新开始
    restartBtn.addEventListener('click', function() {
        // 重置表单
        form.reset();
        
        // 隐藏报告部分，显示介绍部分
        reportSection.classList.add('hidden');
        introSection.classList.remove('hidden');
    });
    
    // 初始化显示第一个问题
    showQuestion(0);
});
