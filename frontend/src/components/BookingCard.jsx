const BookingCard = ({ booking }) => {
  if (!booking) return null;

  const fields = [
    { label: 'Name', value: booking.name, icon: 'M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z' },
    { label: 'Email', value: booking.email, icon: 'M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z' },
    { label: 'Date', value: booking.date, icon: 'M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z' },
    { label: 'Time', value: booking.time, icon: 'M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z' },
  ];

  return (
    <div className="ml-11 mt-3 animate-fade-in-up">
      <div className="max-w-[80%] bg-gradient-to-br from-green-500/20 to-emerald-500/20 border border-green-500/50 rounded-2xl p-4 space-y-3">
        <div className="flex items-center gap-2">
          <div className="w-6 h-6 rounded-full bg-green-500 flex items-center justify-center">
            <svg className="w-4 h-4 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
            </svg>
          </div>
          <span className="text-sm font-semibold text-green-400">Booking Confirmed</span>
        </div>

        <div className="grid grid-cols-2 gap-3">
          {fields.map((field) => (
            <div key={field.label} className="space-y-1">
              <div className="flex items-center gap-1.5 text-xs text-gray-400">
                <svg className="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d={field.icon} />
                </svg>
                <span>{field.label}</span>
              </div>
              <p className="text-sm font-medium text-white">
                {field.value || <span className="text-gray-500 italic">Not provided</span>}
              </p>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default BookingCard;
