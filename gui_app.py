import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import customtkinter as ctk
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import threading
import time
from datetime import datetime
import json
import os

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class CloudPulsePro(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("CloudPulse Pro: AI CostOps Dashboard")
        self.geometry("1200x800")
        self.minsize(1000, 700)

        # Configure grid layout
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Create main container
        self.main_frame = ctk.CTkFrame(self, corner_radius=10)
        self.main_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_rowconfigure(1, weight=1)

        # Header
        self.header_frame = ctk.CTkFrame(self.main_frame, height=60, corner_radius=10)
        self.header_frame.grid(row=0, column=0, sticky="ew", padx=10, pady=10)
        
        self.title_label = ctk.CTkLabel(self.header_frame, text="CloudPulse Pro", font=("Arial", 24, "bold"))
        self.title_label.pack(side="left", padx=20)
        
        self.status_label = ctk.CTkLabel(self.header_frame, text="Status: Active", text_color="green", font=("Arial", 12))
        self.status_label.pack(side="right", padx=20)

        # Main content area
        self.content_frame = ctk.CTkFrame(self.main_frame, corner_radius=10)
        self.content_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)
        self.content_frame.grid_columnconfigure(0, weight=1)
        self.content_frame.grid_rowconfigure(1, weight=1)

        # Tab control
        self.tab_control = ctk.CTkTabview(self.content_frame)
        self.tab_control.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        # Dashboard Tab
        self.dashboard_tab = self.tab_control.add("Dashboard")
        self.setup_dashboard_tab()

        # Analytics Tab
        self.analytics_tab = self.tab_control.add("Analytics")
        self.setup_analytics_tab()

        # Recommendations Tab
        self.recommendations_tab = self.tab_control.add("Recommendations")
        self.setup_recommendations_tab()

        # Settings Tab
        self.settings_tab = self.tab_control.add("Settings")
        self.setup_settings_tab()

        # Status bar
        self.status_bar = ctk.CTkFrame(self.main_frame, height=30)
        self.status_bar.grid(row=2, column=0, sticky="ew", padx=10, pady=5)
        
        self.status_message = ctk.CTkLabel(self.status_bar, text="Ready", font=("Arial", 10))
        self.status_message.pack(side="left", padx=10)
        
        self.last_update = ctk.CTkLabel(self.status_bar, text=f"Last update: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", font=("Arial", 10))
        self.last_update.pack(side="right", padx=10)

        # Start telemetry thread
        self.running = True
        self.telemetry_thread = threading.Thread(target=self.update_telemetry, daemon=True)
        self.telemetry_thread.start()

    def setup_dashboard_tab(self):
        self.dashboard_tab.grid_columnconfigure(0, weight=1)
        self.dashboard_tab.grid_rowconfigure(0, weight=1)
        
        # Create top frame for metrics
        metrics_frame = ctk.CTkFrame(self.dashboard_tab)
        metrics_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        
        # Current spend
        current_spend_frame = ctk.CTkFrame(metrics_frame, width=200, height=100, corner_radius=10)
        current_spend_frame.grid(row=0, column=0, padx=5, pady=5)
        
        ctk.CTkLabel(current_spend_frame, text="Current Spend", font=("Arial", 12, "bold")).pack(pady=(5,0))
        self.current_spend_value = ctk.CTkLabel(current_spend_frame, text="$4,287.56", font=("Arial", 24))
        self.current_spend_value.pack()
        ctk.CTkLabel(current_spend_frame, text="30-day period", font=("Arial", 10)).pack(pady=(0,5))
        
        # Forecasted spend
        forecasted_spend_frame = ctk.CTkFrame(metrics_frame, width=200, height=100, corner_radius=10)
        forecasted_spend_frame.grid(row=0, column=1, padx=5, pady=5)
        
        ctk.CTkLabel(forecasted_spend_frame, text="Forecasted Spend", font=("Arial", 12, "bold")).pack(pady=(5,0))
        self.forecasted_spend_value = ctk.CTkLabel(forecasted_spend_frame, text="$5,123.89", font=("Arial", 24))
        self.forecasted_spend_value.pack()
        ctk.CTkLabel(forecasted_spend_frame, text="Next 30 days", font=("Arial", 10)).pack(pady=(0,5))
        
        # Potential savings
        potential_savings_frame = ctk.CTkFrame(metrics_frame, width=200, height=100, corner_radius=10)
        potential_savings_frame.grid(row=0, column=2, padx=5, pady=5)
        
        ctk.CTkLabel(potential_savings_frame, text="Potential Savings", font=("Arial", 12, "bold")).pack(pady=(5,0))
        self.potential_savings_value = ctk.CTkLabel(potential_savings_frame, text="$1,236.40", font=("Arial", 24, "bold"), text_color="green")
        self.potential_savings_value.pack()
        ctk.CTkLabel(potential_savings_frame, text="Based on recommendations", font=("Arial", 10)).pack(pady=(0,5))
        
        # Cloud distribution
        cloud_dist_frame = ctk.CTkFrame(metrics_frame, width=200, height=100, corner_radius=10)
        cloud_dist_frame.grid(row=0, column=3, padx=5, pady=5)
        
        ctk.CTkLabel(cloud_dist_frame, text="Cloud Distribution", font=("Arial", 12, "bold")).pack(pady=(5,0))
        self.cloud_dist_value = ctk.CTkLabel(cloud_dist_frame, text="AWS: 56% | Azure: 32% | GCP: 12%", font=("Arial", 12))
        self.cloud_dist_value.pack()
        ctk.CTkLabel(cloud_dist_frame, text="Last hour", font=("Arial", 10)).pack(pady=(0,5))
        
        # Charts frame
        charts_frame = ctk.CTkFrame(self.dashboard_tab)
        charts_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=(0,10))
        charts_frame.grid_columnconfigure(0, weight=1)
        charts_frame.grid_rowconfigure(0, weight=1)
        
        # Create chart tabs
        self.chart_tabs = ctk.CTkTabview(charts_frame)
        self.chart_tabs.grid(row=0, column=0, sticky="nsew")
        
        # Spend trend chart
        spend_tab = self.chart_tabs.add("Spend Trend")
        self.setup_spend_chart(spend_tab)
        
        # Anomalies chart
        anomalies_tab = self.chart_tabs.add("Anomalies")
        self.setup_anomalies_chart(anomalies_tab)
        
        # Heatmap tab
        heatmap_tab = self.chart_tabs.add("Heatmap")
        self.setup_heatmap_chart(heatmap_tab)
    
    def setup_spend_chart(self, parent_frame):
        fig, ax = plt.subplots(figsize=(10, 4))
        data = {
            'Date': pd.date_range(start='2023-01-01', periods=30, freq='D'),
            'Spend': np.random.randint(100, 500, size=30).cumsum()
        }
        df = pd.DataFrame(data)
        ax.plot(df['Date'], df['Spend'], marker='o', color='#1f77b4')
        ax.set_title('30-Day Cloud Spend Trend', fontsize=12)
        ax.set_xlabel('Date')
        ax.set_ylabel('Spend ($)')
        ax.grid(True)
        ax.fill_between(df['Date'], df['Spend'], alpha=0.2, color='#1f77b4')
        
        canvas = FigureCanvasTkAgg(fig, master=parent_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    
    def setup_anomalies_chart(self, parent_frame):
        fig, ax = plt.subplots(figsize=(10, 4))
        
        anomalies = {
            'Date': pd.to_datetime(['2023-01-05', '2023-01-12', '2023-01-18', '2023-01-24']),
            'Amount': [125, 320, 415, 280],
            'Severity': ['Low', 'Medium', 'High', 'Medium']
        }
        
        colors = {'Low': 'green', 'Medium': 'orange', 'High': 'red'}
        
        for date, amount, severity in zip(anomalies['Date'], anomalies['Amount'], anomalies['Severity']):
            ax.scatter(date, amount, color=colors[severity], s=150, label=severity if severity not in ax.get_legend_handles_labels()[1] else '')
        
        ax.set_title('Detected Cost Anomalies', fontsize=12)
        ax.set_xlabel('Date')
        ax.set_ylabel('Anomaly Amount ($)')
        ax.grid(True)
        ax.legend()
        
        canvas = FigureCanvasTkAgg(fig, master=parent_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    
    def setup_heatmap_chart(self, parent_frame):
        fig, ax = plt.subplots(figsize=(10, 4))
        
        cloud_services = ['EC2', 'S3', 'RDS', 'Lambda', 'EKS']
        days = [f'Day {i}' for i in range(1, 31)]
        data = np.random.rand(len(cloud_services), len(days))
        
        im = ax.imshow(data, cmap='YlOrRd')
        ax.set_xticks(np.arange(len(days)))
        ax.set_yticks(np.arange(len(cloud_services)))
        ax.set_xticklabels(days, rotation=45, ha='right', fontsize=8)
        ax.set_yticklabels(cloud_services, fontsize=8)
        ax.set_title('Cloud Service Usage Heatmap (Last 30 Days)', fontsize=12)
        
        fig.colorbar(im, ax=ax, label='Relative Cost')
        
        canvas = FigureCanvasTkAgg(fig, master=parent_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    
    def setup_analytics_tab(self):
        self.analytics_tab.grid_columnconfigure(0, weight=1)
        self.analytics_tab.grid_rowconfigure(0, weight=1)
        
        analytics_main_frame = ctk.CTkFrame(self.analytics_tab, corner_radius=10)
        analytics_main_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        analytics_main_frame.grid_columnconfigure(0, weight=1)
        analytics_main_frame.grid_rowconfigure(0, weight=1)
        
        # Cloud breakdown section
        cloud_breakdown_frame = ctk.CTkFrame(analytics_main_frame, corner_radius=10)
        cloud_breakdown_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        
        ctk.CTkLabel(cloud_breakdown_frame, text="Cloud Provider Breakdown", font=("Arial", 14, "bold")).pack(pady=(10,5), anchor="w", padx=10)
        
        # Pie chart
        fig = plt.figure(figsize=(6, 4))
        ax = fig.add_subplot(111)
        
        sizes = [56, 32, 12]
        labels = ['AWS (56%)', 'Azure (32%)', 'GCP (12%)']
        colors = ['#FF9900', '#0089D6', '#4285F4']
        explode = (0.1, 0, 0)
        
        ax.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%', shadow=True, startangle=140)
        ax.set_title('Cloud Provider Distribution')
        ax.axis('equal')
        
        canvas = FigureCanvasTkAgg(fig, master=cloud_breakdown_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=10, pady=(0,10))
        
        # Service breakdown section
        service_breakdown_frame = ctk.CTkFrame(analytics_main_frame, corner_radius=10)
        service_breakdown_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
        
        ctk.CTkLabel(service_breakdown_frame, text="Service Breakdown", font=("Arial", 14, "bold")).pack(pady=(10,5), anchor="w", padx=10)
        
        # Treeview for service costs
        columns = ('Service', 'Cost', 'Percentage')
        self.service_tree = ttk.Treeview(service_breakdown_frame, columns=columns, show='headings', height=10)
        
        # Style the treeview
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview", background="#2B2B2B", foreground="white", fieldbackground="#2B2B2B", borderwidth=0)
        style.configure("Treeview.Heading", background="#3B3B3B", foreground="white", relief="flat")
        style.map("Treeview", background=[('selected', '#1A6EBC')])
        
        for col in columns:
            self.service_tree.heading(col, text=col)
            self.service_tree.column(col, width=100, anchor='center')
        
        # Sample data
        services = [
            ('EC2', 1850.50, '43.2%'),
            ('S3', 980.25, '22.9%'),
            ('RDS', 650.75, '15.2%'),
            ('Lambda', 450.30, '10.5%'),
            ('EKS', 354.76, '8.2%')
        ]
        
        for service in services:
            self.service_tree.insert('', tk.END, values=service)
        
        self.service_tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0,10))
        
        # Cost drivers section
        cost_drivers_frame = ctk.CTkFrame(analytics_main_frame, corner_radius=10)
        cost_drivers_frame.grid(row=1, column=0, columnspan=2, sticky="nsew", padx=10, pady=10)
        
        ctk.CTkLabel(cost_drivers_frame, text="Top Cost Drivers", font=("Arial", 14, "bold")).pack(pady=(10,5), anchor="w", padx=10)
        
        # Bar chart for cost drivers
        fig = plt.figure(figsize=(10, 4))
        ax = fig.add_subplot(111)
        
        drivers = ['Over-provisioned EC2', 'Orphaned volumes', 'Idle RDS instances', 'Unused S3 buckets', 'Scheduled non-prod']
        cost = [750.25, 420.50, 380.75, 210.90, 190.30]
        
        bars = ax.bar(drivers, cost, color='#1A6EBC', alpha=0.7)
        ax.set_title('Top 5 Cost Drivers')
        ax.set_ylabel('Potential Savings ($)')
        ax.set_xticks(range(len(drivers)))
        ax.set_xticklabels(drivers, rotation=45, ha='right', fontsize=8)
        
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                    f'${height:,.2f}',
                    ha='center', va='bottom', fontsize=8)
        
        canvas = FigureCanvasTkAgg(fig, master=cost_drivers_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=10, pady=(0,10))
    
    def setup_recommendations_tab(self):
        self.recommendations_tab.grid_columnconfigure(0, weight=1)
        self.recommendations_tab.grid_rowconfigure(0, weight=1)
        
        # Create main frame
        rec_main_frame = ctk.CTkFrame(self.recommendations_tab, corner_radius=10)
        rec_main_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        rec_main_frame.grid_columnconfigure(0, weight=1)
        rec_main_frame.grid_rowconfigure(1, weight=1)
        
        # Header
        ctk.CTkLabel(rec_main_frame, text="AI-Powered Cost Optimization Recommendations", font=("Arial", 16, "bold")).grid(row=0, column=0, sticky="w", padx=20, pady=10)
        
        # Treeview for recommendations
        columns = ('Priority', 'Recommendation', 'Service', 'Savings', 'Complexity', 'Action')
        self.rec_tree = ttk.Treeview(rec_main_frame, columns=columns, show='headings', height=15)
        
        # Style the treeview
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview", background="#2B2B2B", foreground="white", fieldbackground="#2B2B2B", borderwidth=0)
        style.configure("Treeview.Heading", background="#3B3B3B", foreground="white", relief="flat")
        style.map("Treeview", background=[('selected', '#1A6EBC')])
        
        # Configure columns
        self.rec_tree.heading('Priority', text='Priority')
        self.rec_tree.heading('Recommendation', text='Recommendation')
        self.rec_tree.heading('Service', text='Service')
        self.rec_tree.heading('Savings', text='Savings')
        self.rec_tree.heading('Complexity', text='Complexity')
        self.rec_tree.heading('Action', text='Action')
        
        self.rec_tree.column('Priority', width=50, anchor='center')
        self.rec_tree.column('Recommendation', width=300)
        self.rec_tree.column('Service', width=80, anchor='center')
        self.rec_tree.column('Savings', width=80, anchor='center')
        self.rec_tree.column('Complexity', width=80, anchor='center')
        self.rec_tree.column('Action', width=100, anchor='center')
        
        # Sample recommendations
        recommendations = [
            ('1', 'Downsize over-provisioned EC2 instances (m5.xlarge → m5.large)', 'EC2', '$450/mo', 'Low', 'Review'),
            ('2', 'Delete 5 unattached EBS volumes older than 90 days', 'EBS', '$380/mo', 'Low', 'Delete'),
            ('3', 'Convert 3 idle RDS instances to serverless configuration', 'RDS', '$230/mo', 'Medium', 'Schedule'),
            ('4', 'Archive infrequently accessed S3 objects to Glacier', 'S3', '$150/mo', 'Low', 'Migrate'),
            ('5', 'Right-size Kubernetes worker nodes in EKS cluster', 'EKS', '$125/mo', 'Medium', 'Plan'),
            ('6', 'Purchase Reserved Instances for predictable workloads', 'EC2', '$175/mo', 'High', 'Analyze'),
            ('7', 'Clean up orphaned snapshots in AWS Backup', 'Backup', '$90/mo', 'Low', 'Delete'),
            ('8', 'Optimize Lambda memory allocation based on usage', 'Lambda', '$85/mo', 'Medium', 'Configure'),
            ('9', 'Implement S3 lifecycle policies for log files', 'S3', '$65/mo', 'Low', 'Implement'),
            ('10', 'Enable auto-scaling for EC2 web tier', 'EC2', '$75/mo', 'Medium', 'Enable')
        ]
        
        for rec in recommendations:
            self.rec_tree.insert('', tk.END, values=rec)
        
        self.rec_tree.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)
        
        # Button frame
        button_frame = ctk.CTkFrame(rec_main_frame)
        button_frame.grid(row=2, column=0, sticky="ew", padx=10, pady=10)
        
        ctk.CTkButton(button_frame, text="Implement Selected", command=self.implement_recommendation).pack(side="left", padx=5)
        ctk.CTkButton(button_frame, text="Schedule Implementation", command=self.schedule_recommendation).pack(side="left", padx=5)
        ctk.CTkButton(button_frame, text="Generate Report", command=self.generate_report).pack(side="right", padx=5)
    
    def implement_recommendation(self):
        selected = self.rec_tree.selection()
        if not selected:
            messagebox.showwarning("No Selection", "Please select a recommendation to implement")
            return
        
        item = self.rec_tree.item(selected[0])
        messagebox.showinfo("Implementation", f"Implementing recommendation: {item['values'][1]}")
        
    def schedule_recommendation(self):
        selected = self.rec_tree.selection()
        if not selected:
            messagebox.showwarning("No Selection", "Please select a recommendation to schedule")
            return
        
        item = self.rec_tree.item(selected[0])
        messagebox.showinfo("Scheduled", f"Scheduled for implementation: {item['values'][1]}")
        
    def generate_report(self):
        messagebox.showinfo("Report", "PDF report with all recommendations generated successfully")
    
    def setup_settings_tab(self):
        self.settings_tab.grid_columnconfigure(0, weight=1)
        self.settings_tab.grid_rowconfigure(0, weight=1)
        
        settings_frame = ctk.CTkFrame(self.settings_tab, corner_radius=10)
        settings_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        
        # Connection settings
        conn_frame = ctk.CTkFrame(settings_frame, corner_radius=10)
        conn_frame.pack(fill="x", padx=10, pady=10)
        
        ctk.CTkLabel(conn_frame, text="Cloud Connections", font=("Arial", 14, "bold")).pack(anchor="w", padx=10, pady=(10,5))
        
        # AWS settings
        aws_frame = ctk.CTkFrame(conn_frame)
        aws_frame.pack(fill="x", padx=20, pady=5)
        
        ctk.CTkLabel(aws_frame, text="AWS Account", font=("Arial", 12)).grid(row=0, column=0, sticky="w", padx=5)
        self.aws_key_var = ctk.StringVar(value="AKIAXXXXXXXXXXXXXXXX")
        ctk.CTkEntry(aws_frame, textvariable=self.aws_key_var, width=300).grid(row=0, column=1, sticky="ew", padx=5)
        
        ctk.CTkLabel(aws_frame, text="Region", font=("Arial", 12)).grid(row=1, column=0, sticky="w", padx=5)
        self.aws_region_var = ctk.StringVar(value="us-east-1")
        ctk.CTkComboBox(aws_frame, variable=self.aws_region_var, values=["us-east-1", "us-west-2", "eu-west-1"], width=150).grid(row=1, column=1, sticky="w", padx=5)
        
        # Azure settings
        azure_frame = ctk.CTkFrame(conn_frame)
        azure_frame.pack(fill="x", padx=20, pady=5)
        
        ctk.CTkLabel(azure_frame, text="Azure Subscription", font=("Arial", 12)).grid(row=0, column=0, sticky="w", padx=5)
        self.azure_sub_var = ctk.StringVar(value="xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx")
        ctk.CTkEntry(azure_frame, textvariable=self.azure_sub_var, width=300).grid(row=0, column=1, sticky="ew", padx=5)
        
        # GCP settings
        gcp_frame = ctk.CTkFrame(conn_frame)
        gcp_frame.pack(fill="x", padx=20, pady=5)
        
        ctk.CTkLabel(gcp_frame, text="GCP Project", font=("Arial", 12)).grid(row=0, column=0, sticky="w", padx=5)
        self.gcp_project_var = ctk.StringVar(value="my-gcp-project-123456")
        ctk.CTkEntry(gcp_frame, textvariable=self.gcp_project_var, width=300).grid(row=0, column=1, sticky="ew", padx=5)
        
        # Dashboard preferences
        pref_frame = ctk.CTkFrame(settings_frame, corner_radius=10)
        pref_frame.pack(fill="x", padx=10, pady=10)
        
        ctk.CTkLabel(pref_frame, text="Dashboard Preferences", font=("Arial", 14, "bold")).pack(anchor="w", padx=10, pady=(10,5))
        
        self.dark_mode_var = ctk.BooleanVar(value=True)
        ctk.CTkCheckBox(pref_frame, text="Dark Mode", variable=self.dark_mode_var, command=self.toggle_dark_mode).pack(anchor="w", padx=20, pady=5)
        
        self.notify_var = ctk.BooleanVar(value=True)
        ctk.CTkCheckBox(pref_frame, text="Enable Notifications", variable=self.notify_var).pack(anchor="w", padx=20, pady=5)
        
        ctk.CTkLabel(pref_frame, text="Refresh Interval (minutes)", font=("Arial", 12)).pack(anchor="w", padx=20, pady=(10,5))
        
        self.refresh_interval_var = ctk.StringVar(value="5")
        ctk.CTkComboBox(pref_frame, variable=self.refresh_interval_var, values=["1", "5", "15", "30", "60"]).pack(anchor="w", padx=20, pady=5)
        
        # Button frame
        button_frame = ctk.CTkFrame(settings_frame)
        button_frame.pack(fill="x", padx=20, pady=20)
        
        ctk.CTkButton(button_frame, text="Save Settings", command=self.save_settings).pack(side="right", padx=10)
        ctk.CTkButton(button_frame, text="Test Connections", command=self.test_connections).pack(side="right", padx=10)
        
    def toggle_dark_mode(self):
        if self.dark_mode_var.get():
            ctk.set_appearance_mode("Dark")
        else:
            ctk.set_appearance_mode("Light")
    
    def save_settings(self):
        messagebox.showinfo("Settings", "All settings saved successfully")
    
    def test_connections(self):
        messagebox.showinfo("Connection Test", "Testing connections to cloud providers...\n\nAWS: Connected\nAzure: Connected\nGCP: Connected")
    
    def update_telemetry(self):
        """Simulate telemetry updates"""
        while self.running:
            time.sleep(5)
            
            current_spend = round(np.random.uniform(4000, 4500), 2)
            forecasted_spend = round(current_spend * np.random.uniform(1.1, 1.25), 2)
            potential_savings = round(np.random.uniform(1200, 1400), 2)
            
            self.current_spend_value.configure(text=f"${current_spend:,.2f}")
            self.forecasted_spend_value.configure(text=f"${forecasted_spend:,.2f}")
            self.potential_savings_value.configure(text=f"${potential_savings:,.2f}")
            
            aws_perc = np.random.randint(50, 60)
            azure_perc = np.random.randint(25, 35)
            gcp_perc = 100 - aws_perc - azure_perc
            
            self.cloud_dist_value.configure(text=f"AWS: {aws_perc}% | Azure: {azure_perc}% | GCP: {gcp_perc}%")
            
            self.last_update.configure(text=f"Last update: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            
    def on_closing(self):
        self.running = False
        self.destroy()

if __name__ == "__main__":
    app = CloudPulsePro()
    app.protocol("WM_DELETE_WINDOW", app.on_closing)
    app.mainloop()