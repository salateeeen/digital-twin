type StatusCardProps = {label:string,
                        value:number|null,
                        unit:string
                        };

function StatusCard({label,value,unit}:StatusCardProps){
    return(
        <div className="metric-card">
            <h3>{label}</h3>
            <p>{value !==null ? value : "N/A"}
               {value !==null && <span>{unit}</span>}</p>
        </div>
    )

}
export default StatusCard;