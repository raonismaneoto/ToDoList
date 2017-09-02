function Task(data) {
    this.name = data.name || '';
    this.description = data.description || '';
    this.deadline = data.deadline || '';
    this.state = data.state || '';
};