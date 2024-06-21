function drawPieChart() {
    const canvas = document.getElementById('winRateChart');
    if (!canvas) {
        console.error('Canvas element not found');
        return;
    }
    
    const ctx = canvas.getContext('2d');
    if (!ctx) {
        console.error('Failed to get canvas context');
        return;
    }

    const statisticsElement = document.querySelector('.customStatistics');
    if (!statisticsElement) {
        console.error('Statistics element not found');
        return;
    }

	const totalGames = parseInt(statisticsElement.dataset.totalGames);
	if (!totalGames) {
		//logic for drawing pie chart when there are no games played
		const data = [
			{ label: 'No Games Played', value: 100, color: '#181818' }
		];
		const totalValue = data.reduce((sum, item) => sum + item.value, 0);
		let startAngle = 0;
		data.forEach((item) => {
			const sliceAngle = (item.value / totalValue) * 2 * Math.PI;
			ctx.beginPath();
			ctx.moveTo(canvas.width / 2, canvas.height / 2);
			ctx.arc(canvas.width / 2, canvas.height / 2, Math.min(canvas.width / 2, canvas.height / 2), startAngle, startAngle + sliceAngle);
			ctx.closePath();
			ctx.fillStyle = item.color;
			ctx.fill();
			startAngle += sliceAngle;
		}
		);
        return;
    }
    const winRate = parseFloat(statisticsElement.dataset.winRate);
    const lossRate = 100 - winRate;

    const data = [
        { label: 'Win Rate', value: winRate, color: '#75ff75' },
        { label: 'Loss Rate', value: lossRate, color: '#ff4040' }
    ];

    const totalValue = data.reduce((sum, item) => sum + item.value, 0);

    let startAngle = 0;

    data.forEach((item) => {
        const sliceAngle = (item.value / totalValue) * 2 * Math.PI;

        ctx.beginPath();
        ctx.moveTo(canvas.width / 2, canvas.height / 2);
        ctx.arc(canvas.width / 2, canvas.height / 2, Math.min(canvas.width / 2, canvas.height / 2), startAngle, startAngle + sliceAngle);
        ctx.closePath();
        ctx.fillStyle = item.color;
        ctx.fill();

        startAngle += sliceAngle;
    });

    startAngle = 0;
    data.forEach((item) => {
        const sliceAngle = (item.value / totalValue) * 2 * Math.PI;
        const percentage = Math.round((item.value / totalValue) * 100);

        const labelX = canvas.width / 2 + (Math.min(canvas.width / 2, canvas.height / 2) / 1.5) * Math.cos(startAngle + sliceAngle / 2);
        const labelY = canvas.height / 2 + (Math.min(canvas.width / 2, canvas.height / 2) / 1.5) * Math.sin(startAngle + sliceAngle / 2);

        ctx.fillStyle = '#000000';
		//make it bold
		ctx.font = 'bold 12px Virgil';
        ctx.textAlign = 'center';
        ctx.fillText(percentage + '%', labelX, labelY);

        startAngle += sliceAngle;
    });

}

const initialObserver = new MutationObserver((mutations, obs) => {
    mutations.forEach((mutation) => {
        mutation.addedNodes.forEach((node) => {
            if (node.nodeType === 1 && node.id === 'placeCanvas') {
                drawPieChart();
            }
        });
    });
});

const contentElement = document.getElementById('content');
if (contentElement) {
    initialObserver.observe(contentElement, {
        childList: true,
        subtree: true
    });
} else {
    console.error('Content element not found');
}