window.onload = function () {
    document.getElementById("download")
        .addEventListener("click", () => {
            const invoice = this.document.getElementById("invoice");
            console.log(invoice);
            console.log(window);

            var script_tag = document.getElementById('pdf')
            var username = script_tag.getAttribute("username") + "-Report"

            var opt = {
                margin: 2,
                filename: username,
                image: { type: 'jpeg', quality: 0.98 },
                html2canvas: { scale: 2 },
                jsPDF: { unit: 'in', format: 'tabloid', orientation: 'landscape' }
            };
            html2pdf().from(invoice).set(opt).save();
        })
}