var started = false;
        var completed = false;
        var inprogress = false;
        var ref = 0;

            // Assuming group_quiz.start_time and group_quiz.end_time are already defined as datetime fields in the context
            const startTime = new Date("{{ group_quiz.start_time | date:'Y-m-d\\TH:i:s' }}");
            const endTime = new Date("{{ group_quiz.end_time | date:'Y-m-d\\TH:i:s' }}");
        
            setInterval(function() {
                const currentTime = new Date(); // Get the current time
        
                if (currentTime >= startTime && currentTime <= endTime) {
                    // Quiz is in progress
                    const timeDiff = endTime.getTime() - currentTime.getTime(); // Calculate the difference between current time and end time
        
                    if (timeDiff <= 0) {
                        clearInterval(); // Stop the timer if end time has passed
                        if (ref < 1){
                            document.getElementById("timer").innerHTML = "Completed"; 
                            ref = ref +1;
                        }
                        // Update the timer element with a message
                        completed  = true;
                    } else {
                        started = true;
                        document.getElementById('quiz-main').style.display = 'block'
                        //display the quiz here

                        const diffInSeconds = Math.floor(timeDiff / 1000);
                        const diffInMinutes = Math.floor(diffInSeconds / 60);
                        const diffInHours = Math.floor(diffInMinutes / 60);
        
                        const remainingHours = diffInHours % 24;
                        const remainingMinutes = diffInMinutes % 60;
                        const remainingSeconds = diffInSeconds % 60;
        
                        const formattedTime =
                            "Ends in " +
                            remainingHours +
                            " hours, " +
                            remainingMinutes +
                            " minutes, " +
                            remainingSeconds +
                            " seconds";
        
                        document.getElementById("timer").innerHTML = formattedTime; // Update the timer element with the remaining time
                    }
                } else if (currentTime < startTime) {
                    
                    // Quiz has not started yet
                    const timeDiff = startTime.getTime() - currentTime.getTime(); // Calculate the difference between current time and start time
        
                    const diffInSeconds = Math.floor(timeDiff / 1000);
                    const diffInMinutes = Math.floor(diffInSeconds / 60);
                    const diffInHours = Math.floor(diffInMinutes / 60);
        
                    const remainingDays = Math.floor(diffInHours / 24);
                    const remainingHours = diffInHours % 24;
                    const remainingMinutes = diffInMinutes % 60;
                    const remainingSeconds = diffInSeconds % 60;
        
                    const formattedTime =
                        "Starts in " +
                        remainingDays +
                        " days, " +
                        remainingHours +
                        " hours, " +
                        remainingMinutes +
                        " minutes, " +
                        remainingSeconds +
                        " seconds";
        
                    document.getElementById("timer").innerHTML = formattedTime; // Update the timer element with the remaining time to start
                } else {
                    // Quiz has already ended
                    clearInterval(); // Stop the timer
                    document.getElementById("timer").innerHTML = "Completed"; // Update the timer element with a message
                }
            }, 1000);
            if (started){
                document.getElementById('quiz-main').style.display = 'block'
            }