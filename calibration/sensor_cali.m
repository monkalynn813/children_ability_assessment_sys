function [beta,r_sq]= sensor_cali(volt,torq)
    %volt: voltage data from data acqusition ;array shape: Nx1
    %torq: actual torque applied on torque sensor;array shape: Nx1
    lv=size(volt);
    lt=size(torq);
    if lv(1)~= lt(1)
        error("data size mismatch")
    else
        one_temp=ones(lv);
        volt_temp=[one_temp volt];
        [beta,~,~,~,status]=regress(torq,volt_temp);
        r_sq=status(1);
        figure
        plot(volt,torq,'.');
        hold on
        plot(volt,beta(1)+beta(2)*volt);
        title('Linear Regression for Torque vs. Volt');
        xlabel('Voltage');
        ylabel('Torque');
        grid on
        hold off
    end
    
end
