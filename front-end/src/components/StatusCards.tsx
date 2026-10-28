type StatusCardProps = {label:string,
                        value:number|string|null,
                        unit:string
                        };

function StatusCard({label,value,unit}:StatusCardProps){
    return(
        <div className="metric-card">
            <h3>{label}</h3>
            <p>{value !==null ? value : "No reading"}
              {value !== null && unit !== "" && <span>{unit}</span>}</p>
        </div>
    )

}
export default StatusCard;